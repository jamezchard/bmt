from __future__ import annotations

from asyncio import Queue
from dataclasses import dataclass
from typing import ClassVar, Iterable, Iterator

from rich.style import Style
from rich.text import Text, TextType

from textual import work
from textual.worker import Worker, WorkerCancelled, WorkerFailed, get_current_worker
from textual.message import Message
from textual.reactive import var
from textual.widgets import Tree
from textual.widgets.tree import TreeNode

TOGGLE_STYLE = Style.from_meta({"toggle": True})


class BookMarkPath:
    def __init__(self, id: str, type: str, label: str) -> None:
        self.id = id
        self.type = type
        self.label = label
        self.children = []
        self.loaded: bool = False

    def __str__(self) -> str:
        return f"id {self.id}, type {self.type}, label {self.label}, children {len(self.children)}"


@dataclass
class BookMarkEntry:
    path: BookMarkPath
    loaded: bool = False


class BookMarkTree(Tree[BookMarkEntry]):
    COMPONENT_CLASSES: ClassVar[set[str]] = {
        "bookmark-tree--extension",
        "bookmark-tree--file",
        "bookmark-tree--folder",
        "bookmark-tree--hidden",
    }

    DEFAULT_CSS = """
    BookMarkTree > .bookmark-tree--folder {
        text-style: bold;
    }

    BookMarkTree > .bookmark-tree--extension {
        text-style: italic;
    }

    BookMarkTree > .bookmark-tree--hidden {
        color: $text 50%;
    }
    """

    path: var[BookMarkPath] = var[BookMarkPath](
        BookMarkPath(0, "T", "RootDir"),
        init=False,
        always_update=True,
    )

    class MarkSelected(Message, bubble=True):
        def __init__(self, node: TreeNode[BookMarkEntry], path: BookMarkPath) -> None:
            super().__init__()
            self.node: TreeNode[BookMarkEntry] = node
            self.path: BookMarkPath = path

        @property
        def control(self) -> Tree[BookMarkEntry]:
            return self.node.tree

    def __init__(
        self,
        path: BookMarkPath,
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        self._load_queue: Queue[TreeNode[BookMarkEntry]] = Queue()
        super().__init__(
            path.label,
            data=BookMarkEntry(path),
            name=name,
            id=id,
            classes=classes,
            disabled=disabled,
        )
        self.path = path

    def _add_to_load_queue(self, node: TreeNode[BookMarkEntry]) -> None:
        assert node.data is not None
        if not node.data.loaded:
            node.data.loaded = True
            self._load_queue.put_nowait(node)

    def reload(self) -> None:
        self.reset(self.path.label, BookMarkEntry(self.path))
        self._load_queue = Queue()
        self._loader()
        self._add_to_load_queue(self.root)

    def watch_path(self) -> None:
        # raise RuntimeError
        self.reload()

    def process_label(self, label: TextType) -> Text:
        if isinstance(label, str):
            text_label = Text(label)
        else:
            text_label = label
        first_line = text_label.split()[0]
        return first_line

    def render_label(self, node: TreeNode[BookMarkEntry], base_style: Style, style: Style) -> Text:
        node_label = node._label.copy()
        node_label.stylize(style)

        if node._allow_expand:
            prefix = ("📂 " if node.is_expanded else "📁 ", base_style + TOGGLE_STYLE)
            node_label.stylize_before(
                self.get_component_rich_style("bookmark-tree--folder", partial=True)
            )
        else:
            prefix = ("📄 ", base_style)
            node_label.stylize_before(
                self.get_component_rich_style("bookmark-tree--file", partial=True)
            )
            node_label.highlight_regex(
                r"\..+$", self.get_component_rich_style("bookmark-tree--extension", partial=True)
            )

        if node_label.plain.startswith("."):
            node_label.stylize_before(self.get_component_rich_style("bookmark-tree--hidden"))

        text = Text.assemble(prefix, node_label)
        return text

    @staticmethod
    def _safe_is_dir(path: BookMarkPath) -> bool:
        return True if path.type == "T" else False

    def _populate_node(
        self, node: TreeNode[BookMarkEntry], content: Iterable[BookMarkPath]
    ) -> None:
        node.remove_children()
        for path in content:
            node.add(path.label, data=BookMarkEntry(path), allow_expand=self._safe_is_dir(path))
        node.expand()

    def _directory_content(self, location: BookMarkPath, worker: Worker) -> Iterator[BookMarkPath]:
        try:
            for entry in location.children:
                if worker.is_cancelled:
                    break
                yield entry
        except PermissionError:
            pass

    @work
    def _load_directory(self, node: TreeNode[BookMarkEntry]) -> list[BookMarkPath]:
        """Load the directory contents for a given node.

        Args:
            node: The node to load the directory contents for.

        Returns:
            The list of entries within the directory associated with the node.
        """
        assert node.data is not None
        return self._directory_content(node.data.path, get_current_worker())
        # return sorted(
        #     self._directory_content(node.data.path, get_current_worker()),
        #     key=lambda path: (not self._safe_is_dir(path), path.label),
        # )

    @work(exclusive=True)
    async def _loader(self) -> None:
        """Background loading queue processor."""
        worker = get_current_worker()
        while not worker.is_cancelled:
            # Get the next node that needs loading off the queue. Note that
            # this blocks if the queue is empty.
            node = await self._load_queue.get()
            content: list[BookMarkPath] = []
            try:
                # Spin up a short-lived thread that will load the content of
                # the directory associated with that node.
                content = await self._load_directory(node).wait()
            except WorkerCancelled:
                # The worker was cancelled, that would suggest we're all
                # done here and we should get out of the loader in general.
                break
            except WorkerFailed:
                # This particular worker failed to start. We don't know the
                # reason so let's no-op that (for now anyway).
                pass
            else:
                # We're still here and we have directory content, get it into
                # the tree.
                if content:
                    self._populate_node(node, content)
            # Mark this iteration as done.
            self._load_queue.task_done()

    def _on_tree_node_expanded(self, event: Tree.NodeExpanded) -> None:
        event.stop()
        dir_entry = event.node.data
        if dir_entry is None:
            return
        if self._safe_is_dir(dir_entry.path):
            self._add_to_load_queue(event.node)
        else:
            self.post_message(self.MarkSelected(event.node, dir_entry.path))

    def _on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        event.stop()
        dir_entry = event.node.data
        if dir_entry is None:
            return
        if not self._safe_is_dir(dir_entry.path):
            self.post_message(self.MarkSelected(event.node, dir_entry.path))
