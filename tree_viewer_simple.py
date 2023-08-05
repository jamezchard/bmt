from pathlib import Path
from rich.text import Text
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Tree
from textual.widgets.tree import TreeNode

import yaml


class TreeApp(App):
    def compose(self) -> ComposeResult:
        yield Tree("Root")

    @classmethod
    def add_yaml(cls, node: TreeNode, yaml_data: object) -> None:
        from rich.highlighter import ReprHighlighter

        highlighter = ReprHighlighter()

        def add_node(name: str, node: TreeNode, data: object) -> None:
            """Adds a node to the tree.

            Args:
                name (str): Name of the node.
                node (TreeNode): Parent node.
                data (object): Data associated with the node.
            """
            if isinstance(data, dict):
                node.set_label(Text(f"{{}} {name}"))
                for key, value in data.items():
                    new_node = node.add("")
                    add_node(key, new_node, value)
            elif isinstance(data, list):
                node.set_label(Text(f"[] {name}"))
                for index, value in enumerate(data):
                    new_node = node.add("")
                    add_node(str(index), new_node, value)
            else:
                node.allow_expand = False
                if name:
                    label = Text.assemble(
                        Text.from_markup(f"[b]{name}[/b]="), highlighter(repr(data))
                    )
                else:
                    label = Text(repr(data))
                node.set_label(label)

        add_node("YAML", node, yaml_data)

    def on_mount(self) -> None:
        """Load some YAML when the app starts."""
        file_path = Path(__file__).parent / "prj.yaml"
        with open(file_path, mode="r", encoding="utf-8") as data_file:
            self.yaml_data = yaml.load(data_file, Loader=yaml.Loader)
        tree = self.query_one(Tree)
        tree.show_root = False
        self.action_add()

    def action_add(self) -> None:
        """Add a node to the tree."""
        tree = self.query_one(Tree)
        yaml_node = tree.root.add("YAML")
        self.add_yaml(yaml_node, self.yaml_data)
        tree.root.expand()

    def action_clear(self) -> None:
        """Clear the tree (remove all nodes)."""
        tree = self.query_one(Tree)
        tree.clear()


if __name__ == "__main__":
    app = TreeApp()
    app.run()
