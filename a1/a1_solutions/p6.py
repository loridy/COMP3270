import sys, parse, grader

def number_of_attacks(problem):
    #Your p6 code here
    
    queens = []
    for row in range(8):
        for col in range(8):
            if problem[row][col] == 'q':
                queens.append([row, col])
    ans = []
    for row in range(8):
        line = ""
        for col in range(8):
            tmr = [x[:] for x in queens]
            count = 0
            for _ in tmr:
                if _[1] == col:
                    _[0] = row 
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

            if col == 0:
                if count >= 10: line = str(count)
                else: line = " "+str(count)
            else:
                if count >= 10: line = line+" "+str(count)
                else: line = line+"  "+str(count)
        ans.append(line)
    solution = "\n".join(ans)

    return solution


if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 6
    grader.grade(problem_id, test_case_id, number_of_attacks, parse.read_8queens_search_problem)