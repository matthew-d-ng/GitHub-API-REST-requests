import getpass
from grabHotspots import grab_repo_files
from grabHotspots import Git_file
from grabHotspots import code_churn
from github import Github

username = raw_input("Enter github username: ")
password = getpass.getpass("Password: ")
g = Github(username, password)

if g is not None:
    file_commits = grab_repo_files(g, "XanthusXX/MedicalApp")

    print "success"

    for f in file_commits:
        print "%s: commits=%d, lines=%d, %s, churn=%d" \
            % (f.name, f.commits_size, f.lines, f.authors, f.code_churn)

else:
    print "unsuccessful"
