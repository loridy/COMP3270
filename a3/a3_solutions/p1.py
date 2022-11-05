import sys, grader, parse
import random


score = 0.0
def play_episode(problem):
    global score
    score = 0.0
    # initialization
    seed = problem["seed"]
    if seed != -1:
        random.seed(seed, version=1)
    noise = problem["noise"]
    livingReward = problem["livingReward"]
    grid = problem["grid"]
    policy = problem["policy"]
    player_position = tuple()
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col]=="S":
                player_position=(row, col)
    experience = []
    # preparation
    experience.append("Start state:")
    state = show_grid(grid, player_position)
    experience.append(state)
    experience.append("Cumulative reward sum: "+str(score))

    # start
    # first, getting next move(with policy known)
    # second, identify reward
    while True:
        experience.append("-------------------------------------------- ")
        
        # get next move
        p_row, p_col = player_position
        intended = policy[p_row][p_col]
        next = next_move(grid, player_position, intended, noise)
        experience.append("Taking action: {} (intended: {})".format(next, intended))
        player_position = update_player(grid, player_position, next, livingReward)
        p_row, p_col = player_position

        # update reward
        experience.append("Reward received: {}".format(livingReward))
        
        # show grid
        experience.append("New state:")
        state = show_grid(grid, player_position)
        experience.append(state)

        # update score
        score += livingReward
        experience.append("Cumulative reward sum: "+str(round(score,2)))
        
        # goal state
        if policy[p_row][p_col] == "exit":
            experience.append("-------------------------------------------- ")
            final_reward = float(grid[p_row][p_col])
            experience.append("Taking action: exit (intended: exit)")
            experience.append("Reward received: {}".format(final_reward))
            experience.append("New state:")
            tmr = []
            for row in grid:
                tmr.append("".join(["{:>5}".format(col) for col in row]))
            experience.append("\n".join(tmr))
            score += final_reward
            experience.append("Cumulative reward sum: "+str(round(score,2)))
            break
    f = open("./file.txt", "w")
    f.write("\n".join(experience))
    f.close()
    return "\n".join(experience)


def next_move(grid, player_position, intended, noise):
    possible_move = {"N":["N", "E", "W"], "E":["E", "S", "N"], "S":["S", "W", "E"], "W":["W", "N", "S"]}
    next = random.choices(population=possible_move[intended], weights=[1-noise*2, noise, noise])[0]
    return next

def update_player(grid, player_position, next, livingReward, ):

    movements = {'N': (-1, 0), 'S': (1, 0), 'W': (0, -1), 'E': (0, 1)}
    p_row, p_col = player_position
    r, c = movements[next]
    # out of index
    # hit wall
    tmr_r, tmr_c = p_row+r, p_col+c
    if tmr_r not in range(len(grid)) or tmr_c not in range(len(grid[0])):
        return player_position
    if grid[tmr_r][tmr_c]== "#":
        return player_position
    player_position = (tmr_r, tmr_c)
    return player_position

def show_grid(grid, player_position):
    r, c = player_position
    tmr_grid = [line[:] for line in grid]
    tmr_grid[r][c] = "P"
    tmr = []
    for row in tmr_grid:
        tmr.append("".join(["{:>5}".format(col) for col in row]))
    return "\n".join(tmr)



if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    #test_case_id = 1
    problem_id = 1
    grader.grade(problem_id, test_case_id, play_episode, parse.read_grid_mdp_problem_p1)