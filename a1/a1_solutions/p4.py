import sys, parse, grader
from heapq import heappop, heappush
def greedy_search(problem):
    #Your p4 code here
    # print("---------------- p4: ---------------- ")
    startState = problem["startState"]
    goalState = problem["goalState"]
    graph = problem["graph"]
    heuristic = problem["heuristic"]

    frontier = []
    heappush(frontier, (heuristic[startState], [startState]))
    exploredSet = set()
    # print("Initial frontier: ", frontier)
    # print()
    exploredOrder = []
    while frontier:
        node = heappop(frontier)
        # print("node", node)
        if node[1][-1] in goalState:
            # print("Found answer: ")
            ans = " ".join(exploredOrder)+"\n"+" ".join(node[1])
            # print(ans)
            return ans
        if node[1][-1] not in exploredSet:
            # print("Exploring ", node[1][-1], "at cost ", node[0])
            exploredOrder.append(node[1][-1])
            exploredSet.add(node[1][-1])
            for child in graph[node[1][-1]]:
                heappush(frontier, (heuristic[child[1]], node[1]+[child[1]]))
        # print("frontier: ", list(frontier))
        # print("exploredSet: ", exploredSet)
        # print("exploredOrder", exploredOrder)
        # print()

    solution = 'S B D C\nS C G'
    return solution

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 4
    grader.grade(problem_id, test_case_id, greedy_search, parse.read_graph_search_problem)