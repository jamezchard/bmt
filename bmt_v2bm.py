"""
做 VS 到 BMT 的信息传递
"""

from tkinter import messagebox
from pathlib import Path
from utils import (
    get_repo_dir,
    get_repo_info,
    bmt_root,
    convert_path,
    dprint,
    mark_yaml,
    org_fine_grain,
    org_coarse_grain,
)


import shutil
import sys
import yaml


def v2bm(src_pth: Path, line: int, label=None) -> None:
    src_pth = Path(Path(src_pth).resolve().as_posix())
    dprint(f"{src_pth} {line}")

    # --------------------------------------------------------------------------------
    # 1. 拿 git 仓库信息，working tree 不干净则退出
    # --------------------------------------------------------------------------------
    repo_dir = get_repo_dir(src_pth)
    if not repo_dir:
        # TODO(ckclr): error should always print
        messagebox.showinfo("hello bmt", f"no .git/ found in {src_pth}'s ancestors")
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
    mark_table: dict[int | str, int | str] = {}
    mark_id = 0
    mark_pos = f"{src_pth},{line}"
    if commit_dir.exists():  # commit dir 存在就认为 table file 存在
        dprint(f"commit_dir exsits:\n{commit_dir}")
        with open(table_fn, mode="r", encoding="utf-8") as table_file:
            mark_table = yaml.load(table_file, Loader=yaml.Loader)
        if mark_table is None:  # 可能被清空过，是个空文件
            mark_id = 0
            mark_table = {mark_id: mark_pos}
            mark_table["max_id"] = mark_id
        elif mark_pos in mark_table.values():
            for k, v in mark_table.items():
                if v == mark_pos:
                    mark_id = k
                    break
            messagebox.showinfo("hello bmt", f"{mark_pos} already exsits, will use old id")
        else:
            mark_id = int(mark_table["max_id"]) + 1
            mark_table[mark_id] = mark_pos
            mark_table["max_id"] = mark_id

    else:
        dprint(f"commit_dir creating:\n{commit_dir}")
        commit_dir.mkdir(parents=True)
        mark_id = 0
        mark_table = {mark_id: mark_pos}
        mark_table["max_id"] = mark_id
    with open(table_fn, mode="w", encoding="utf-8") as table_file:
        yaml.dump(mark_table, table_file, Dumper=yaml.Dumper)

    # use 2 org files, one is for fine grain marks and the other is for coarse grain call stacks
    org_fn = prj_dir / (org_fine_grain if label is None else org_coarse_grain)
    if org_fn.exists():
        org_file = open(org_fn, mode="a+", encoding="utf-8")
    else:
        org_file = open(org_fn, mode="w", encoding="utf-8")
        org_file.write(":PROPERTIES:\n")
        org_file.write(f":REPO:     {repo_dir.resolve().as_posix()}\n")
        org_file.write(f":SHA:      {hexsha}\n")
        org_file.write(":END:\n\n")

    with open(src_pth, mode="r", encoding="utf-8") as src_file:
        if label is None:
            label = src_file.readlines()[line - 1]
            label = (" ".join(label.strip().split()))[:80]

    org_file.write(f"\n* [[elisp:(ckclr/bmt-bm2v)][{mark_id:0>8}]] -- {label}\n")
    org_file.close()

    # copy source file as a backup
    tgt_pth = commit_dir / convert_path(src_pth)
    if not tgt_pth.exists():
        shutil.copy(src_pth, tgt_pth)


def main():
    v2bm(Path(sys.argv[1]), int(sys.argv[2]))


if __name__ == "__main__":
    main()
