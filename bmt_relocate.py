from pathlib import Path
from utils import get_repo_info
from tkinter import messagebox


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
    # 1. v2bm 时把 source file 也 copy 过来
    # 2. 基于某种 diff 算法做匹配
    pass


if __name__ == "__main__":
    main()
