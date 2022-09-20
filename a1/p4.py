import sys, parse, grader

def greedy_search(problem):
    #Your p4 code here
    solution = 'S B D C\nS C G'
    return solution

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 4
    grader.grade(problem_id, test_case_id, greedy_search, parse.read_graph_search_problem)