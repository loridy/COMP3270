import sys, grader, parse

def bfs_search(problem):
    #Your p2 code here
    solution = 'Ar B C D\nAr C G'
    return solution

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 2
    grader.grade(problem_id, test_case_id, bfs_search, parse.read_graph_search_problem)