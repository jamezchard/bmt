from git.repo import Repo
from common import *


def get_repo_info(repo_dir):
    repo = Repo(repo_dir)
    # print(repo.heads)
    # print(repo.head.commit.hexsha)
    # print(repo.active_branch.commit.hexsha)

    # 获取 git interface，可以直接调用 git 命令
    # 基础命令用 git.command()，比如 git.stash(), git.branch()
    # 额外参数传到 command 的参数中，比如 git.stash("pop", "stash@{0}"), git.branch("-D", "branch-name")
    # git_itf = repo.git
    # git_itf.stash()
    # git_itf.stash("pop", "stash@{0}")
    return repo.active_branch.commit.hexsha, repo.is_dirty()


def copy_source_file(src_file: Path, repo_dir: Path, prj_dir: Path):
    """
    保证 copy 的是 unmodified 的源码，目前方案是先 git stash 然后 copy 最后在 git stash pop 回来，
    但是可能引起 Visual Studio 的重编译。另一种方式是用 repo.index.diff(None)[0].a_path 把修改过的文件
    copy 到临时目录，然后 git reset 最后 copy 回来
    """
    if not src_file.is_relative_to(repo_dir):
        return
    hexsha, is_dirty = get_repo_info(repo_dir)
    dst_dir = prj_dir / hexsha
    if not dst_dir.exists():
        dst_dir.mkdir(parents=True)
    dst_file = dst_dir / convert_path(src_file)
    dprint(f"copying {src_file} to {dst_file}")
    if is_dirty:
        git_itf = Repo(repo_dir).git
        git_itf.stash()  # 假设是 blocking 调用
        shutil.copyfile(src_file, dst_file)
        git_itf.stash("pop", "stash@{0}")
    else:  # 不需要多余的 stash
        shutil.copyfile(src_file, dst_file)


if __name__ == "__main__":
    get_repo_info(Path(sys.argv[1]))
