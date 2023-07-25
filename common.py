from pathlib import Path
from tkinter import messagebox
import shutil
import sys
import os

debug = False
bmt_root = Path("D:/bmt-prj")
dprint = lambda x: print(x) if debug else None


def get_repo_dir(in_pth: Path):
    in_pth = Path(in_pth)
    cwd = in_pth if in_pth.is_dir() else in_pth.parent
    while True:
        dprint(cwd)
        for pth in cwd.iterdir():
            if pth.is_dir() and pth.name == ".git":
                return cwd
        if cwd == cwd.parent:
            dprint("no .git/ found until root")
            return None
        else:
            cwd = cwd.parent


def convert_path(pth: Path):
    """
    convert D:\AB\CD\EF to D=+AB+CD+EF
    """
    return str(Path(pth).as_posix()).replace(":", "=").replace("/", "+")
