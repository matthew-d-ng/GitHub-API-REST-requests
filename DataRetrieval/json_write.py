import json
from grabHotspots import Git_tree_node
from grabHotspots import Git_file


def json_from_git_tree(tree):

    files = []
    links = []
    if tree.ftype != "tree":
        print "writing ", tree.data.name
        file_data = {
                "file": tree.data.name,
                "type": "file",
                "lines": tree.data.lines,
                "commits": tree.data.commits_size,
                "churn": tree.data.code_churn,
                "commit_stats": [],  # [additions, lines]
                "authors": []            # [author, churn]
            }

        for auth, stat in tree.data.authors.iteritems():
            file_data["authors"].append( [auth, stat] )

        for commit in tree.data.commits:
            file_data["commit_stats"].append( [ commit[0], commit[1] ] )

        files.append( file_data )

    else:
        print "writing ", tree.data
        file_data = {
                "file": tree.data,
                "type": "dir",
                "lines": 0,
                "commits": 0,
                "churn": 0,
                "commit_stats": [],
                "authors": [],
            }
        files.append( file_data )

        for child in tree.children:

            target = ""
            if child.ftype == "tree":
                target = child.data
            else:
                target = child.data.name

            link = {
                "source": tree.data, "target": target
            }
            # write link
            links.append( link )
            new_json = json_from_git_tree(child)
            files = files + new_json[0]
            links = links + new_json[1]

    with open('links.json', 'w') as outfile:
        json.dump(links, outfile)

    with open('files.json', 'w') as outfile:
        json.dump(files, outfile)

    return (files, links)

