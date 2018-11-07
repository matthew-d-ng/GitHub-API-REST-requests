import operator
from github import Github


# param:   Github instance,
#          name of repository 'user/repo_name'
#
# return:  List of tuples - (user, additions, deletions)

def grab_lines_of_code(gh_instance, repo_name):

    base_repo = gh_instance.get_repo(repo_name)
    user_list = dict()

    print base_repo.name
    print "running..."

    for contribution in base_repo.get_stats_contributors():
        user = contribution.author.login
        for week in contribution.weeks:
            if user in user_list:
                additions = user_list[user][0]
                deletions = user_list[user][1]
                user_list[user] = [additions + week.a, deletions + week.d]
            else:
                user_list[user] = [week.a, week.d]

    user_tup = list()
    for user, code in user_list.items():
        user_tup.append( (user, code[0], code[1]) )

    return sorted( user_tup, key=operator.itemgetter(1), reverse=True )

