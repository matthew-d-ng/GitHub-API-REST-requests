import getpass
import json
from grabHotspots import grab_repo_files
from grabHotspots import Git_tree_node
from grabHotspots import Git_file
from json_write import json_from_git_tree
from github import Github

def print_tree(tree_node, prefix="  "):

    if tree_node.ftype != "tree":
        f = tree_node.data
        print "%s%s: commits=%d, lines=%d, %s, churn=%d" \
                    % (prefix, f.name, f.commits_size, f.lines, f.authors, f.code_churn)

    else:
        print prefix + tree_node.data
        for child in tree_node.children:
            print_tree( child, prefix + "   ")


username = raw_input("Enter github username: ")
password = getpass.getpass("Password: ")
g = Github(username, password)

if g is not None:
    file_commits = grab_repo_files(g, "matthew-d-ng/HaskellProblems")

    print "success"

    # print_tree( file_commits )

    json_from_git_tree( file_commits )


else:
    print "unsuccessful"
