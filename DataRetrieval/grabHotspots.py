from github import Github

class file:

    def __init__(self, commits, lines, authors):
        self.commits = commits
        self.lines = lines
        

def grab_repo_files(gh_instance, repo_name):

    base_repo = gh_instance.get_repo(repo_name)
    print base_repo.name, "\n"

    commit_list = base_repo.get_commits()
    last_commit = commit_list[0]
    root_sha = last_commit.sha

    tree = base_repo.get_git_tree(root_sha, recursive=True)
    file_commits = grab_files(base_repo, tree)

    for file, commits in file_commits.iteritems():
        print "%s : %d" % (file, commits)


def grab_files(repo, tree):

    file_commits = dict()
    for node in tree.tree:
        if node.type != "tree":
            commits = repo.get_commits(path=node.path)
            commit_amount = commits.totalCount
            file_commits[node.path] = commit_amount
    return file_commits

