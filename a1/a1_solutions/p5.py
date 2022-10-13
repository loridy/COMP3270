import sys, parse, grader
from heapq import heappush, heappop
def astar_search(problem):
    #Your p5 code here
    startState = problem["startState"]
    goalState = problem["goalState"]
    graph = problem["graph"]
    heuristic = problem["heuristic"]

    frontier = []
    heappush(frontier, (heuristic[startState], [startState]))
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
                heappush(frontier, (node[0]+child[0]+(heuristic[child[1]]-heuristic[node[1][-1]]), node[1]+[child[1]]))

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 5
    grader.grade(problem_id, test_case_id, astar_search, parse.read_graph_search_problem)