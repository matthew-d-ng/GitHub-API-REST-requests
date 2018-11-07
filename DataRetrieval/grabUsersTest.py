import sys
import unittest
from github import Github
from grabUsers import grab_lines_of_code


def test_known(gh_instance):
    # Can't really test the data coming in, since we don't know
    # what will arrive. Can only test a known return.

    # A relatively small repository that shouldn't change
    # We can therefore predict the values and check the results

    repo_stats = grab_lines_of_code(g, "matthew-d-ng/CS3012_graph")

    # should return a list of tuples
    # list should only have one element

    assert repo_stats is not None, "TestKnown: Testing NULL"
    assert len(repo_stats) == 1, "TestKnown: Testing length == 1"

    user = repo_stats[0]
    assert user[0] == "matthew-d-ng", "Testing only known member of repo"

    assert user[1] == 416, "Testing known line additions"

    assert user[2] == 208, "Testing known line deletions"

    # visually testing printing information
    print_stats(repo_stats)


def test_large_unknown(gh_instance):
    # We can't predict data so we'll just make sure it doesn't break

    repo_stats = grab_lines_of_code(g, "PyGithub/PyGithub")

    assert repo_stats is not None, "TestUnknown: Testing NULL"

    # visually testing printing information
    print_stats(repo_stats)


def print_stats(repo_stats):
    for tup in repo_stats:
        print "%20s: \t+%8d \t-%8d" % tup


# main

g = None

if len(sys.argv) == 3:
    g = Github( sys.argv[1], sys.argv[2] )
else:
    g = Github()

test_known(g)
print "Finished test_known\n"

test_large_unknown(g)
print "Finished test_large_unknown\n"


