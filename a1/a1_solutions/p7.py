import sys, parse, grader
from p6 import number_of_attacks
def better_board(problem):
    queens = []
    for row in range(8):
        for col in range(8):
            if problem[row][col] == 'q':
                queens.append([row, col])
    count = number_of_attacks(problem)
    graph = [line.split() for line in count.split("\n")]
    intGraph = [[int(i) for i in line] for line in graph]
    mininum = min([min(line) for line in intGraph])
    for row in range(8):
        for col in range(8):
            if int(intGraph[row][col]) == mininum:
                for queen in queens:
                    if queen[1] == col:
                        problem[queen[0]][col] = "."
                        problem[row][col] = "q"
                        solution = "\n".join([" ".join(line) for line in problem])
                        return solution

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 7
    grader.grade(problem_id, test_case_id, better_board, parse.read_8queens_search_problem)