from pathlib import Path
from utils import get_repo_info
from tkinter import messagebox

import sys


def relocate(org_fn: Path):
    """
    repo sha 和 org sha 对比，不同时做行号重定位 (mark-table.yaml 中)
    """
    with open(org_fn, mode="r", encoding="utf-8") as org_file:
        repo_dir = None
        hexsha_local = None
        repo_prop = ":REPO:"
        sha_prop = ":SHA:"
        for line in org_file:
            line = line.strip()
            if line.startswith(repo_prop):
                repo_dir = line.replace(repo_prop, "").strip()
            if line.startswith(sha_prop):
                hexsha_local = line.replace(sha_prop, "").strip()

    assert repo_dir is not None and hexsha_local is not None
    hexsha_remote, is_dirty = get_repo_info(repo_dir)
    if is_dirty:
        messagebox.showinfo("hello bmt", "repo is dirty, bm is not allowed")
        return
    if hexsha_remote == hexsha_local:
        messagebox.showinfo("hello bmt", "repo has no changes, no need to relocate")
        return

    # TODO(ckclr):
    # 在 remote 文件中以 local 记录的 line number 为起点向上和向下做文本相似性匹配 (比如 Jaro–Winkler similarity)
    # 设置一个最大半径和最小分数，在最大半径内没找到高于最小分数的匹配，那就寻找失败，说明这行代码被删了
    pass
    


if __name__ == "__main__":
    relocate(Path(sys.argv[1]))
