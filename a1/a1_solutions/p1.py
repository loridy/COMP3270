from cmath import exp
import sys, grader, parse
import collections

def dfs_search(problem):
    #Your p1 code here

    startState = problem["startState"]
    goalState = problem["goalState"]
    graph = problem["graph"]

    frontier = collections.deque([[startState]])
    exploredSet = set()
    exploredOrder = []
    while frontier:
        node = frontier.pop()
        if node[-1] in goalState:
            solution = " ".join(exploredOrder) + "\n" + " ".join(node)
            return solution
        if node[-1] not in exploredSet:
            exploredOrder.append(node[-1])
            exploredSet.add(node[-1])
            for child in graph[node[-1]]:
                frontier.append(node+[child[1]])



if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 1
    grader.grade(problem_id, test_case_id, dfs_search, parse.read_graph_search_problem)