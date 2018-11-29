# GitHub API REST requests
Using **Python** to retrieve data from the Github API and eventually processing this data into nice visualisations using d3.js library.

# Information Displayed
The visualisation displays a graph with several nodes, representing files within a repository, whose size corresponds to the amount of lines within them. The colour of the nodes displays their "heat", i.e the amount of commits that have affected them. The number on the node represents the code churn. Clicking a node will open up further information about that file, including: a graph over time of it's size and also raw additions ( essentially code churn over time ) and the code churn of each contributor in respect to that particular file.
