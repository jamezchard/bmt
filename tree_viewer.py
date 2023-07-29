from dataclasses import dataclass
from pathlib import Path
from textual.app import App, ComposeResult
from textual.widgets import DirectoryTree
from textual.message import Message
from pprint import pprint

import yaml


class BookMarkPath:
    def __init__(self, id: str, type: str, label: str) -> None:
        self.id = id
        self.type = type
        self.label = label
        self.children = None
        self.loaded = False

    def iter_child(self) -> "BookMarkPath":
        if self.children is None:
            return
        for child in self.children:
            yield child

    def __str__(self) -> str:
        return (
            f"id {self.id}, type {self.type}, label {self.label}, "
            f"#children {0 if self.children is None else len(self.children)}"
        )


def construct_book_mark_path(data: object) -> BookMarkPath | list[BookMarkPath]:
    if isinstance(data, list):  # 子目录列表
        return [construct_book_mark_path(node) for node in data]
    elif isinstance(data, dict):  # 节点元信息
        path = BookMarkPath(data["id"], data["type"], data["label"])
        if data["type"] == "T" and data["children"] is not None:
            path.children = construct_book_mark_path(data["children"])
        return path
    else:
        raise RuntimeError("UKN data")


def print_book_mark_path(path: BookMarkPath | list[BookMarkPath], depth):
    indent = "\t" * depth
    if isinstance(path, BookMarkPath):
        print(indent + str(path))
        if path.type == "T" and path.children is not None:
            for p in path.children:
                print_book_mark_path(p, depth + 1)
    else:
        for p in path:
            print(indent + str(p))
            if p.type == "T" and p.children is not None:
                for q in p.children:
                    print_book_mark_path(q, depth + 1)


class BookMarkTree(DirectoryTree):
    class MarkSelected(Message):
        pass


class BookMarkTreeApp(App):
    def compose(self) -> ComposeResult:
        yield DirectoryTree("D:/tree-view")

    def on_directory_tree_file_selected(self, event: BookMarkTree.MarkSelected) -> None:
        raise RuntimeError("on_directory_tree_file_selected")


if __name__ == "__main__":
    # app = BookMarkTreeApp()
    # app.run()

    with open("prj.yaml", mode="r", encoding="utf-8") as yf:
        data = yaml.load(yf, Loader=yaml.Loader)
    bmt = construct_book_mark_path(data["transactions"])
    print_book_mark_path(bmt, 0)
