import getpass
from grabHotspots import grab_repo_files
from grabHotspots import Git_file
from github import Github

# not really tests initially but just getting it incrementally "working"

username = raw_input("Enter github username: ")
password = getpass.getpass("Password: ")
g = Github(username, password)

file_commits = grab_repo_files(g, "XanthusXX/MedicalApp")

if g is not None:
    print "success"

for f in file_commits:
    print "%s: commits=%d, lines=%d, %s, churn=%d" \
          % (f.name, f.commits_size, f.lines, f.authors, f.code_churn)
