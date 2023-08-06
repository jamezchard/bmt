from tkinter import messagebox
import sys
import win32com.client

messagebox.showinfo("Hello", sys.argv[1])


def open_file_in_devenv(filename, line):
    dte = win32com.client.GetActiveObject("VisualStudio.DTE")
    dte.MainWindow.Activate
    dte.ItemOperations.OpenFile(filename)
    dte.ActiveDocument.Selection.MoveToLineAndOffset(line, 1)
