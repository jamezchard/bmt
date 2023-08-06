from git.repo import Repo
from pathlib import Path
from tkinter import messagebox

import shutil
import sys
import os

debug = False
dprint = lambda x: messagebox.showinfo("debug", x) if debug else None

bmt_root = Path("D:/bmt-prj")


def open_in_vim():
    line = int(sys.argv[1])
    col = int(sys.argv[2])
    fname = sys.argv[3]
    cli = f'gvim "+call cursor({line}, {col})" "{fname}"'
    print(cli)
    os.system(cli)


def get_repo_dir(in_pth: Path):
    """
    向上找 repo 根目录
    """
    in_pth = Path(in_pth)
    cwd = in_pth if in_pth.is_dir() else in_pth.parent
    while True:
        dprint(cwd)
        if (cwd / ".git").exists():
            return cwd
        elif cwd == cwd.parent:
            dprint(f"no .git/ found until root {cwd}")
            return None
        else:
            cwd = cwd.parent


def convert_path(pth: Path):
    """
    convert D:/AB/CD/EF to D=+AB+CD+EF
    """
    return str(Path(pth).resolve().as_posix()).replace(":", "=").replace("/", "+")


def get_repo_info(repo_dir):
    repo = Repo(repo_dir)
    # print(repo.heads)
    # print(repo.head.commit.hexsha)
    # print(repo.active_branch.commit.hexsha)

    # 获取 git interface，可以直接调用 git 命令
    # 基础命令用 git.command()，比如 git.stash(), git.branch() 额外参数传到 command 的参数中
    # 比如 git.stash("pop", "stash@{0}"), git.branch("-D", "branch-name")
    # git_itf = repo.git
    # git_itf.stash()
    # git_itf.stash("pop", "stash@{0}")
    return repo.active_branch.commit.hexsha, repo.is_dirty()


def copy_src_file(src_file: Path, repo_dir: Path, prj_dir: Path):
    """
    只允许 copy 干净的 working tree
    """
    if not src_file.is_relative_to(repo_dir):
        dprint(f"{src_file} is not relative to {repo_dir}, will not copy")
        return
    hexsha, is_dirty = get_repo_info(repo_dir)
    if is_dirty:
        dprint(f"{repo_dir} is dirty, will not copy")
        return
    dst_dir = prj_dir / hexsha
    if not dst_dir.exists():
        dst_dir.mkdir(parents=True)
    dst_file = dst_dir / convert_path(src_file)
    dprint(f"copying {src_file} to {dst_file}")
    shutil.copyfile(src_file, dst_file)


if __name__ == "__main__":
    repo_dir = get_repo_dir(Path(sys.argv[1]))
    if repo_dir:
        print(repo_dir, get_repo_info(repo_dir))
