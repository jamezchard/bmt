from common import *

import git_utils


def open_in_vim():
    line = int(sys.argv[1])
    col = int(sys.argv[2])
    fname = sys.argv[3]
    cli = f'gvim "+call cursor({line}, {col})" "{fname}"'
    print(cli)
    os.system(cli)


def main():
    line = int(sys.argv[1])
    col = int(sys.argv[2])
    src_pth = Path(sys.argv[3])
    messagebox.showinfo("hello bmt", f"{line} {col} {src_pth}")
    repo_dir = get_repo_dir(src_pth)
    if not repo_dir:
        messagebox.showinfo("hello bmt", "no .git/ found")
        return
    prj_name = convert_path(repo_dir)
    prj_pth = bmt_root / prj_name
    messagebox.showinfo("hello bmt", f"{repo_dir} {prj_pth}")
    if not prj_pth.exists():
        prj_pth.mkdir(parents=True)
    hexsha, is_dirty = git_utils.get_repo_info(repo_dir)
    messagebox.showinfo("hello bmt", f"{hexsha} {is_dirty}")
    commit_dir = prj_pth / hexsha
    if not commit_dir.exists():
        commit_dir.mkdir(parents=True)


if __name__ == "__main__":
    main()
