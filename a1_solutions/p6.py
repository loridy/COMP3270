import sys, parse, grader

def number_of_attacks(problem):
    #Your p6 code here
    
    # create a list of queens
    queens = []
    for row in range(8):
        for col in range(8):
            if problem[row][col] == 'q':
                queens.append([row, col])
    # print(queens)
    ans = []
    for row in range(8):
        line = ""
        for col in range(8):
            tmr = [x[:] for x in queens]
            count = 0
            for _ in tmr:
                if _[1] == col:
                    _[0] = row #  here comes a new list of queens
                    break
            for i in range(7):
                state = tmr.pop()
                for rest in tmr:
                    # row
                    if rest[0] == state[0]: count += 1
                    # upper left to lower right
                    if rest[0] - rest[1] == state[0]-state[1]: count += 1
                    # upper right to lower left
                    if rest[0] + rest[1] == state[0]+state[1]: count += 1
            # print(count, end=" ")

            if col == 0:
                if count >= 10: line = str(count)
                else: line = " "+str(count)
            else:
                if count >= 10: line = line+" "+str(count)
                else: line = line+"  "+str(count)
        # print(line)
        ans.append(line)
    solution = "\n".join(ans)
#     solution = """18 12 14 13 13 12 14 14
# 14 16 13 15 12 14 12 16
# 14 12 18 13 15 12 14 14
# 15 14 14 17 13 16 13 16
# 17 14 17 15 17 14 16 16
# 17 17 16 18 15 17 15 17
# 18 14 17 15 15 14 17 16
# 14 14 13 17 12 14 12 18"""
    return solution


if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 6
    grader.grade(problem_id, test_case_id, number_of_attacks, parse.read_8queens_search_problem)