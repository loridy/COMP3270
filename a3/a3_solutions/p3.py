import sys, grader, parse
import random

score=0.0
def value_iteration(problem):
    global score
    score = 0.0
    # initialization
    discount = problem["discount"]
    noise = problem["noise"]
    livingReward = problem["livingReward"]
    iteration = problem["iteration"]
    grid = problem["grid"]
    player_position = tuple()
    policy = [["" for j in range(len(grid[0]))] for i in range(len(grid))]
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col]=="S":
                grid[row][col] = livingReward
                policy[row][col] = "N"
            elif grid[row][col]=="_":
                grid[row][col] = livingReward
                policy[row][col] = "N"
            elif grid[row][col] == "#":
                policy[row][col] = "#"
            else:
                grid[row][col] = float(grid[row][col])
                policy[row][col] = "x"
    # prepare
    return_value = []
    turn = 0
    return_value.append("V_k=%s" % (turn))
    tmr = []
    for row in grid:
        tmr.append("".join(["|{:7.2f}|".format(0) if row[i]!="#" else "| ##### |" for i in range(len(row))]))
    return_value.append("\n".join(tmr))

    # start
    while True:
        turn += 1
        return_value.append("V_k=%s" % (turn))
        return_value.append(show_grid(grid))
        return_value.append("pi_k=%s" % (turn))
        return_value.append(show_policy(policy))
        grid = v_iteration(grid, policy, discount, noise, livingReward)
        if turn==iteration-1:
            break
    with open("./file.txt", "w") as file:
        file.write("\n".join(return_value))
    return "\n".join(return_value)


def v_iteration(grid, policy, discount, noise, livingReward):
    new_grid=[line[:] for line in grid]
    movements = {'N': (-1, 0), 'S': (1, 0), 'W': (0, -1), 'E': (0, 1)}
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if policy[row][col] == "x" or policy[row][col] == "#":
                continue
            else:
                move, value = get_max(grid, row, col, noise, livingReward, discount)
            new_grid[row][col] = value
            policy[row][col] = move
    return new_grid


def get_max(grid, row, col, noise, livingReward, discount):
    possible_move = {"N":["N", "E", "W"], "E":["E", "S", "N"], "S":["S", "W", "E"], "W":["W", "N", "S"]}
    movements = {'N': (-1, 0), 'S': (1, 0), 'W': (0, -1), 'E': (0, 1)}
    max_value = float("-inf")
    max_move = ""
    for next in movements:
        value = 0
        for n in possible_move[next]:
            r, c = movements[n]
            tmr_r, tmr_c = r+row, c+col
            if tmr_r not in range(len(grid)) or tmr_c not in range(len(grid[0])) or grid[tmr_r][tmr_c]== "#":
                tmr_r, tmr_c = row, col
            if n==next:
                value += (1-2*noise)*(livingReward+discount*grid[tmr_r][tmr_c])
            else:
                value += noise*(livingReward+discount*grid[tmr_r][tmr_c])
        if value > max_value:
            max_value = value
            max_move = next

    return max_move, max_value


def show_grid(grid):
    tmr_grid = [line[:] for line in grid]
    tmr = []
    for row in tmr_grid:
        tmr.append("".join(["|{:7.2f}|".format(col) if col!="#" else "| ##### |"  for col in row]))
    return "\n".join(tmr)


def show_policy(policy):
    tmr_policy = [line[:] for line in policy]
    tmr = []
    for row in tmr_policy:
        tmr.append("".join(["| {} |".format(col) for col in row]))
    return "\n".join(tmr)


if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    #test_case_id = -4
    problem_id = 3
    grader.grade(problem_id, test_case_id, value_iteration, parse.read_grid_mdp_problem_p3)