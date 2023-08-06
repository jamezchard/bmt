"""
做 VS 到 BMT 的信息传递
"""

from tkinter import messagebox
from pathlib import Path
from utils import get_repo_dir, get_repo_info, bmt_root, convert_path, dprint, mark_yaml, org_org
from uuid import uuid1

import sys
import yaml


def main():
    src_pth = Path(sys.argv[1]).resolve().as_posix()
    line = int(sys.argv[2])
    dprint(f"{src_pth} {line}")

    # --------------------------------------------------------------------------------
    # 1. 拿 git 仓库信息，working tree 不干净则退出
    # --------------------------------------------------------------------------------
    repo_dir = get_repo_dir(src_pth)
    if not repo_dir:
        # TODO(ckclr): error should always print
        messagebox.showinfo("hello bmt", "no .git/ found")
        return
    hexsha, is_dirty = get_repo_info(repo_dir)
    if is_dirty:
        messagebox.showinfo("hello bmt", f"repo is dirty, bm is not allowed")
        return

    # --------------------------------------------------------------------------------
    # 2. 处理 mark-table.yaml 文件
    # --------------------------------------------------------------------------------
    prj_dir = bmt_root / convert_path(repo_dir)
    commit_dir: Path = prj_dir / hexsha
    dprint(f"prj_dir {prj_dir}\ncommit_dir {commit_dir}")

    table_fn = commit_dir / mark_yaml
    mark_table: dict[str, str] = {}
    mark_id = str(uuid1())
    mark_pos = f"{src_pth},{line}"
    if commit_dir.exists():
        dprint(f"commit_dir exsits:\n{commit_dir}")
        with open(table_fn, mode="r", encoding="utf-8") as table_file:
            mark_table = yaml.load(table_file, Loader=yaml.Loader)
        if mark_table is None:
            mark_table = {mark_id, mark_pos}
        elif mark_pos in mark_table.values():
            messagebox.showinfo(
                "hello bmt",
                f"{mark_pos} already exsits, will not add to {table_fn}",
            )
            mark_id = None
        else:
            mark_table[mark_id] = mark_pos
    else:
        dprint(f"commit_dir creating:\n{commit_dir}")
        commit_dir.mkdir(parents=True)
        mark_table[mark_id] = mark_pos
    with open(table_fn, mode="w", encoding="utf-8") as table_file:
        yaml.dump(mark_table, table_file, Dumper=yaml.Dumper)

    org_fn = prj_dir / org_org
    if org_fn.exists():
        org_file = open(org_fn, mode="a+", encoding="utf-8")
    else:
        org_file = open(org_fn, mode="w", encoding="utf-8")
        org_file.write(":PROPERTIES:\n")
        org_file.write(f":REPO:     {repo_dir.resolve().as_posix()}\n")
        org_file.write(f":SHA:      {hexsha}\n")
        org_file.write(":END:\n")

    if mark_id:
        with open(src_pth, mode="r", encoding="utf-8") as src_file:
            # TODO(ckclr): check empty label
            label = src_file.readlines()[line - 1]
            label = label.strip()[:50]
            if len(label) == 0:
                label = "EMPTY"
        org_file.write(f"\n* [[elisp:(ckclr/bmt-bm2v)][{label}]]\n")
        org_file.write(":PROPERTIES:\n")
        org_file.write(f":ID:     {mark_id}\n")
        org_file.write(":END:\n")
    else:
        messagebox.showinfo("hello bmt", f"{mark_pos} already exsits, will not add to {org_fn}")
    org_file.close()

    # --------------------------------------------------------------------------------
    # 3. repo sha 和 org sha 对比，不同时做行号重定位 (mark-table.yaml 中)
    # --------------------------------------------------------------------------------
    pass


if __name__ == "__main__":
    main()