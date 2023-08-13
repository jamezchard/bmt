from pathlib import Path
from tkinter import messagebox
from utils import mark_yaml, dprint

import sys
import win32com.client
import yaml


def open_file_in_devenv(filename, line):
    dte = win32com.client.GetActiveObject("VisualStudio.DTE")
    dte.MainWindow.Activate
    dte.ItemOperations.OpenFile(filename)
    dte.ActiveDocument.Selection.MoveToLineAndOffset(line, 1)


def main():
    prj_dir = Path(sys.argv[1]).parent
    hexsha = sys.argv[2]
    mark_id = sys.argv[3]
    # messagebox.showinfo("hello-bmt", f"{prj_dir}\n{hexsha}\n{mark_id}")
    # input mark_id should be like init_default_renderpass(); -- [[elisp:(ckclr/bmt-bm2v)][hUznLpunvjpoFgqWYxNkFK]]
    mark_id = mark_id.split("][")[-1][:-2]
    with open(prj_dir / hexsha / mark_yaml, mode="r", encoding="utf-8") as table_file:
        mark_table = yaml.load(table_file, Loader=yaml.Loader)
        mark_pos = mark_table[mark_id].split(",")
        open_file_in_devenv(mark_pos[0], mark_pos[1])


if __name__ == "__main__":
    main()
