from pathlib import Path
import sys
import os

debug = True

dprint = lambda x: print(x) if debug else None

def get_repo_root(in_pth: Path):
    cwd = in_pth
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


def main():
    line = int(sys.argv[1])
    col = int(sys.argv[2])
    fname = sys.argv[3]
    cli = f'gvim "+call cursor({line}, {col})" "{fname}"'
    print(cli)
    os.system(cli)


if __name__ == "__main__":
    get_repo_root(Path(sys.argv[1]))
