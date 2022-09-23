from cmath import exp
import sys, grader, parse
import collections

def dfs_search(problem):
    #Your p1 code here

    # print("---------------- p1: ---------------- ")
    startState = problem["startState"]
    goalState = problem["goalState"]
    graph = problem["graph"]

    frontier = collections.deque([[startState]])
    exploredSet = set()
    # print("Initial frontier: ", list(frontier))
    # print()
    exploredOrder = []
    while frontier:
        node = frontier.pop()
        # print("node: ", node)
        if node[-1] in goalState:
            # print("Found answer: ")
            ans = " ".join(exploredOrder) + "\n" + " ".join(node)
            # print(ans)
            return ans
        if node[-1] not in exploredSet:
            # print("Exploring node: ", node[-1], "...")
            exploredOrder.append(node[-1])
            exploredSet.add(node[-1])
            for child in graph[node[-1]]:
                frontier.append(node+[child[1]])
        # print("frontier: ", list(frontier))
        # print("exploredSet: ", exploredSet)
        # print("exploredOrder", exploredOrder)
        # print()

    solution = 'Ar D C\nAr C G'
    return solution

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 1
    grader.grade(problem_id, test_case_id, dfs_search, parse.read_graph_search_problem)