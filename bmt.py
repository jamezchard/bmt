import sys
import os


def main():
    line = int(sys.argv[1])
    col = int(sys.argv[2])
    fname = sys.argv[3]
    cli = f'gvim "+call cursor({line}, {col})" "{fname}"'
    print(cli)
    os.system(cli)


if __name__ == "__main__":
    main()
