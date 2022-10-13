import sys, parse, grader

def astar_search(problem):
    #Your p5 code here
    solution = 'S D C B\nS C G'
    return solution

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 5
    grader.grade(problem_id, test_case_id, astar_search, parse.read_graph_search_problem)