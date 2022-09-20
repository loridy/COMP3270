import sys, grader, parse

def dfs_search(problem):
    #Your p1 code here
    solution = 'Ar D C\nAr C G'
    return solution

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 1
    grader.grade(problem_id, test_case_id, dfs_search, parse.read_graph_search_problem)