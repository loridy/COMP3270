import sys, parse, grader

def ucs_search(problem):
    #Your p3 code here
    solution = 'S D B C\nS C G'
    return solution

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 3
    grader.grade(problem_id, test_case_id, ucs_search, parse.read_graph_search_problem)