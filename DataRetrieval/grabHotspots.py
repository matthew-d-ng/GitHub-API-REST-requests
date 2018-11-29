from __future__ import division
from github import Github

class Git_file:

    def __init__(self, name, commits_size, commits, lines, authors, code_churn):
        self.name = name
        self.commits_size = commits_size
        self.commits = commits
        self.lines = lines
        self.authors = authors
        self.code_churn = code_churn


def code_churn(lines, additions):

    if additions == 0 and lines == 0:
        return 0                  # didn't do anything

    if additions == 0:
        return 100              # only deletions
    
    return ((additions - lines) / additions) * 100.0


def grab_repo_files(gh_instance, repo_name):

    base_repo = gh_instance.get_repo(repo_name)
    print base_repo.name, "\n"

    commit_list = base_repo.get_commits()
    last_commit = commit_list[0]
    root_sha = last_commit.sha

    tree = base_repo.get_git_tree(root_sha, recursive=True)
    file_commits = grab_files_from_tree(base_repo, tree)

    return file_commits


def grab_files_from_tree(repo, tree):

    files = list()
    for node in tree.tree:
        if node.type != "tree":

            commits_list = repo.get_commits(path=node.path)
            commit_amount = commits_list.totalCount
            this_file = repo.get_contents(node.path)

            total_lines = 0
            total_additions = 0
            commit_stats = list()
            authors = dict()

            for commit in commits_list:
                commit_lines = 0
                commit_additions = 0
                for content in commit.files:
                    if content.filename == this_file.path:

                        commit_lines += content.additions
                        commit_lines -= content.deletions
                        commit_additions += content.additions
                        total_lines += content.additions
                        total_lines -= content.deletions

                        auth_add = 0
                        auth_lines = 0
                        if commit.author.login in authors:
                            auth_add = authors[commit.author.login][0]
                            auth_lines = authors[commit.author.login][1]

                        authors[commit.author.login] = ( auth_add + commit_additions, 
                                                                             auth_lines + commit_lines )

                        commit_additions = content.additions
                        total_additions += content.additions
                        break

                commit_stats.append( (commit_lines, commit_additions) )

            churn = code_churn(total_lines, total_additions)
            auth_churn = dict()
            for auth, stats in authors.iteritems():
                auth_churn[auth] = code_churn( stats[1], stats[0] )

            new_file = Git_file( this_file.name, commit_amount, commit_stats, \
                                           total_lines, auth_churn, churn )
            files.append( new_file )

    return files
