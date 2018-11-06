import json
import requests
from github import Github

g = Github("1048acd3eab5123dd21513889f1ebff4c4e92043")

for repo in g.get_user().get_repos():

    print repo.name
    contrib_url = repo.contributors_url
    print contrib_url
    
    r = requests.get(contrib_url)
    data = r.json()
    #print data

    print data
