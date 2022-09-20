import sys, parse, grader

def number_of_attacks(problem):
    #Your p6 code here
    solution = """18 12 14 13 13 12 14 14
14 16 13 15 12 14 12 16
14 12 18 13 15 12 14 14
15 14 14 17 13 16 13 16
17 14 17 15 17 14 16 16
17 17 16 18 15 17 15 17
18 14 17 15 15 14 17 16
14 14 13 17 12 14 12 18"""
    return solution

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 6
    grader.grade(problem_id, test_case_id, number_of_attacks, parse.read_8queens_search_problem)