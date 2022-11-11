import sys, grader, parse
import random

score = 0.0
def policy_evaluation(problem):
    global score
    score = 0.0
    # initialization
    discount = problem["discount"]
    noise = problem["noise"]
    livingReward = problem["livingReward"]
    iteration = problem["iteration"]
    grid = problem["grid"]
    policy = problem["policy"]
    player_position = tuple()
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col]=="S":
                player_position=(row, col)
                grid[row][col] = livingReward
            elif grid[row][col]=="_":
                grid[row][col] = livingReward
            elif grid[row][col] != "#":
                grid[row][col] = float(grid[row][col])
    
    # prepare
    return_value = []
    turn = 0
    return_value.append("V^pi_k=%s" % (turn))
    tmr = []
    for row in grid:
        tmr.append("".join(["|{:7.2f}|".format(0) if row[i]!="#" else "| ##### |" for i in range(len(row))]))
    return_value.append("\n".join(tmr))

    # start
    while True:
        turn += 1
        return_value.append("V^pi_k=%s" % (turn))
        return_value.append(show_grid(grid))
        grid = utility(grid, policy, discount, noise, livingReward)
        if turn==iteration-1:
            break
    return "\n".join(return_value)


def utility(grid, policy, discount, noise, livingReward):
    new_grid=[line[:] for line in grid]
    possible_move = {"N":["N", "E", "W"], "E":["E", "S", "N"], "S":["S", "W", "E"], "W":["W", "N", "S"]}
    movements = {'N': (-1, 0), 'S': (1, 0), 'W': (0, -1), 'E': (0, 1)}
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if policy[row][col] == "exit" or policy[row][col] == "#":
                continue
            else:
                next_moves = possible_move[policy[row][col]]
                value = 0
                for next in next_moves:
                    r, c = movements[next]
                    tmr_r, tmr_c = row+r, col+c
                    if tmr_r not in range(len(grid)) or tmr_c not in range(len(grid[0])) or grid[tmr_r][tmr_c]== "#":
                        tmr_r, tmr_c = row, col
                    if next==policy[row][col]:
                        value += (1-2*noise)*(livingReward+discount*grid[tmr_r][tmr_c])
                    else:
                        value += noise*(livingReward+discount*grid[tmr_r][tmr_c])
                new_grid[row][col] = value
    return new_grid


def show_grid(grid):
    # r, c = player_position
    tmr_grid = [line[:] for line in grid]
    # tmr_grid[r][c] = "P"
    tmr = []
    for row in tmr_grid:
        tmr.append("".join(["|{:7.2f}|".format(col) if col!="#" else "| ##### |"  for col in row]))
    return "\n".join(tmr)


if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    #test_case_id = -7
    problem_id = 2
    grader.grade(problem_id, test_case_id, policy_evaluation, parse.read_grid_mdp_problem_p2)