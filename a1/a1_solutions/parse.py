import os, sys

def read_graph_search_problem(file_path):
    with open(file_path) as file:
        lines = file.read().split("\n")
    startState = lines[0].split(": ")[1]
    goalState = lines[1].split(": ")[1].split()
    graph = dict()
    heuristic = dict()
    for i in range(2, len(lines)):
        line = lines[i].split()
        if len(line) == 2:
            heuristic[line[0]] = float(line[1])
        elif len(line) == 3:
            if line[0] in graph:
                graph[line[0]].append((float(line[2]), line[1]))
            else:
                graph[line[0]] = [(float(line[2]), line[1])]
    for state in heuristic:
        if state not in graph:
            graph[state] = []
    problem = dict()
    problem["startState"] = startState
    problem["goalState"] = goalState
    problem["graph"] = graph
    problem["heuristic"] = heuristic

    return problem

def read_8queens_search_problem(file_path):

    with open(file_path) as file:
        lines = file.read().split("\n")
    problem = [line.split() for line in lines]

    return problem

if __name__ == "__main__":
    if len(sys.argv) == 3:
        problem_id, test_case_id = sys.argv[1], sys.argv[2]
        if int(problem_id) <= 5:
            problem = read_graph_search_problem(os.path.join('test_cases','p'+problem_id, test_case_id+'.prob'))
        else:
            problem = read_8queens_search_problem(os.path.join('test_cases','p'+problem_id, test_case_id+'.prob'))
        print(problem)
    else:
        print('Error: I need exactly 2 arguments!')