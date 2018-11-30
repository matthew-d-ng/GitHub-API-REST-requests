import getpass
from grabHotspots import grab_repo_files
from grabHotspots import Git_tree_node
from json_write import json_from_git_tree
from github import Github
from github.GithubException import BadCredentialsException
from github.GithubException import UnknownObjectException
from github.GithubException import RateLimitExceededException

username = raw_input("Enter github username: ")
password = getpass.getpass("Password: ")
g = Github(username, password)

repo = raw_input("Enter repo to read in form 'user/repo': ")

if g is not None:
    try:
        file_commits = grab_repo_files(g, repo)
    except BadCredentialsException:
        print "Your login data was incorrect, please try again... "
        exit()
    except UnknownObjectException:
        print "Are you sure that repo exists? Try put it in again... "
        exit()
    except RateLimitExceededException:
        print "Oh, your rate limit has blocked us, please try again later... "
        exit()

    print "success"

    json_from_git_tree( file_commits )

else:
    print "unsuccessful"
