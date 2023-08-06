import sys
import win32com.client


def main():
    filename = sys.argv[1]
    line = int(sys.argv[2])
    column = int(sys.argv[3])

    dte = win32com.client.GetActiveObject("VisualStudio.DTE")
    dte.MainWindow.Activate
    dte.ItemOperations.OpenFile(filename)
    dte.ActiveDocument.Selection.MoveToLineAndOffset(line, column + 1)


if __name__ == "__main__":
    main()
