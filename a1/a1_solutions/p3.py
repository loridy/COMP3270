import sys, parse, grader
from heapq import heappop, heappush
def ucs_search(problem):
    #Your p3 code here
    startState = problem["startState"]
    goalState = problem["goalState"]
    graph = problem["graph"]

    frontier = []
    heappush(frontier, (0.0, [startState]))
    exploredSet = set()
    exploredOrder = []
    while frontier:
        node = heappop(frontier)
        if node[1][-1] in goalState:
            solution = " ".join(exploredOrder)+"\n"+" ".join(node[1])
            return solution
        if node[1][-1] not in exploredSet:
            exploredOrder.append(node[1][-1])
            exploredSet.add(node[1][-1])
            for child in graph[node[1][-1]]:
                heappush(frontier, (node[0]+child[0], node[1]+[child[1]]))

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 3
    grader.grade(problem_id, test_case_id, ucs_search, parse.read_graph_search_problem)