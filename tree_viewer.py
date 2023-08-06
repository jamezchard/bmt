from dataclasses import dataclass
from pathlib import Path
from textual.app import App, ComposeResult
from pprint import pprint
from book_mark_tree import BookMarkPath, BookMarkTree
from origin_dirtree import DirectoryTree

import yaml


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


class BookMarkTreeApp(App):
    def compose(self) -> ComposeResult:
        with open("prj.yaml", mode="r", encoding="utf-8") as yf:
            data = yaml.load(yf, Loader=yaml.Loader)
        bmt = construct_book_mark_path(data)
        yield BookMarkTree(bmt)
        # yield DirectoryTree("D:/dynamic-dir")

    # def on_book_mark_tree_mark_selected(self, event: BookMarkTree.MarkSelected) -> None:
    #     raise RuntimeError(event.path.label)


if __name__ == "__main__":
    app = BookMarkTreeApp()
    app.run()
