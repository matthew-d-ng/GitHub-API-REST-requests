import getpass
from grabHotspots import grab_repo_files
from github import Github

# not really tests initially but just getting it incrementally "working"

username = raw_input("Enter github username: ")
password = getpass.getpass("Password: ")
g = Github(username, password)

grab_repo_files(g, "matthew-d-ng/CS3012_graph")

if g is not None:
    print "success"
