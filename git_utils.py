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
    只允许 copy 干净的 working tree
    """
    if not src_file.is_relative_to(repo_dir):
        return
    hexsha, is_dirty = get_repo_info(repo_dir)
    if is_dirty:
        return
    dst_dir = prj_dir / hexsha
    if not dst_dir.exists():
        dst_dir.mkdir(parents=True)
    dst_file = dst_dir / convert_path(src_file)
    dprint(f"copying {src_file} to {dst_file}")
    shutil.copyfile(src_file, dst_file)


if __name__ == "__main__":
    get_repo_info(Path(sys.argv[1]))
