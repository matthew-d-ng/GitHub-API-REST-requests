from github import Github

def grab_repo_files(gh_instance, repo_name):

    base_repo = gh_instance.get_repo(repo_name)
    print base_repo.name

    # so, we need the sha of the root of the repo
    # apparently that's not trivially included in the api
    # we have to grab the latest commit to get it

    last_commit = base_repo.get_commits.get_page(0)
    # root_sha = last_commit.

    # tree = base_repo.get_git_tree()
    # print tree
    # grab_files(base_repo, tree)


def grab_files(repo, tree):

    leaf_list = list()
    for node in tree.tree:
        print node.path
        if node.type == "tree":
            sub_tree = repo.get_git_tree(node.sha, recursive=True)
            leaf_list.append( grab_files(repo, sub_tree) )
        elif node.type == "blob":
            leaf_list.append( node.path )

    return leaf_list

