import sys, parse
from turtle import pos
import time, os, copy
import random, math
score = 0
nn = 0
def min_max_mulitple_ghosts(problem, k):
    #Your p5 code here    

    winner = "Ghost"
    global score, nn
    seed, board = problem["seed"], problem["board"]
    nn = sum([r.count(".") for r in board])
    # random.seed(seed, version=1)
    random.seed()
    # add position of existed players, and delete other players
    tmr = {"P": [], "W": [], "X": [], "Y": [], "Z": []}
    positions = dict()    
    for p in tmr:
        position = [[i, board[i].index(p)] for i in range(len(board)) if p in board[i]]
        if len(position) != 0:
            positions[p] = position[0]
    
    # clear board
    for p in positions:
        row, col = positions[p]
        board[row] = board[row][:col]+" "+board[row][col+1:]
    # print("\n".join(board))
    # copy = makeboard(board, positions)
    # print("\n".join(copy))
    # add players

    players = dict()
    i = 0
    for p in positions:
        players[i] = p
        i += 1
    num = len(players)
    turn, score = 0, 0
    solution = []

    # GAME STARTS
    solution.append(f"seed: {seed}")
    solution.append(str(turn))
    solution.append("\n".join(makeboard(board, positions)))
    while True:
        turn += 1
        # if (turn-1)%num == 0:
        #     k -= 1
        # print(turn)
        next = next_move(board, players[(turn-1)%num], positions)
        solution.append(f"{turn}: {players[(turn-1)%num]} moving {next[0]}")
        solution.append(next[1])

        end = check_end(board, players[(turn-1)%num], positions)
        solution.append(f"score: {score}")
        if end=="P":
            solution.append("WIN: Pacman")
            winner = "Pacman"
            break
        if end == "Ghost":
            solution.append("WIN: Ghost")
            break
        # if turn == num*dd:
        #     print("ends", players[(turn-1)%num])
        #     break
    # print(evaluate(board, positions))
    return "\n".join(solution), winner

def get_max(copy_board, player, positions, depth):
    # used by Pacman
    # always get max value/action by choosing from the next player's minimum value/action
    
    board = [row[:] for row in copy_board]
    num_of_food = sum([row.count(".") for row in board])
    # if no food on the board, get positive infinite utility
    if num_of_food == 0: 
        return float("inf")
    g_positions = [positions[g] for g in positions if g!="P"]
    # if pacman on ghosts' location, meanning that it's eaten, so get negative infinite utility
    if positions["P"] in g_positions: 
        return float("-inf") 

    # update tmr board if food eaten, used to check subsequent movements
    pr,pc = positions["P"]
    if board[pr][pc] == ".":
        board[pr] = board[pr][:pc]+" "+board[pr][pc+1:]
    # starts with max value being negative infinite
    # once a action gets higher utility, record the higher utility and corresponding movement
    max_val = float("-inf") 
    possible_move = possible_movements(board, player, positions) 
    next = random.choice(possible_move)
    # print("Pacman searching depth:",depth,"<------------------")
    # go through all possible moves by pacman and finds the maximum evaluation (and record the action)
    for move in possible_move:
        # print("pacman checking:", move)
        tmr_positions = dict()
        for p in positions:
            tmr_positions[p] = positions[p]
        movements = {'N': (-1, 0), 'S': (1, 0), 'W': (0, -1), 'E': (0, 1)}
        # update tmr_positions for the next player
        row, col = tmr_positions[player]
        r, c = movements[move]
        tmr_positions[player] = [row+r, col+c]
        # get expected action(value) chosen by the next player (ghost plays minimum)
        tmr = get_min(board, "W", tmr_positions, depth)
        tmr_min = tmr[0]

        # compare such state with previously stored max_val/movement
        # if evaluation of this action greater than stored action, then replace it
        if tmr_min >= max_val:
            max_val = tmr_min
            next = move

    # print("Pacman finish depth:",depth,"<------------------")
    # print("finding: ", next, "with", max_val)

    # if depth greater than 1, meaning that it's not current depth, so return a value of the evaluation
    # if depth equals 1, meaning that it's current depth, 
    # and therefore should return a action instead of a value
    if depth > 1:
        return max_val
    return next

def get_min(copy_board, player, positions, depth):
    # used by players other than pacman
    # return a value if it is intermediate state; return an action if player is currently playing


    # util represents if previous player eats a food (specifically for pacman)
    util = False 
    board = [row[:] for row in copy_board]
    pr,pc = positions["P"]
    if board[pr][pc] == ".":
        # check last action made by pacman: if it eats a food; if so, change util to True
        board[pr] = board[pc][:pc]+" "+board[pr][pc+1:]
        util = True 
    num_of_food = sum([row.count(".") for row in board])
    # same with get_max: check if game over
    if num_of_food == 0:
        return float("inf"), " "
    g_positions = [positions[g] for g in positions if g!="P"]
    if positions["P"] in g_positions:
        # print("die")
        return float("-inf"), " "
    
    # intitially assign negative infinite to min_val
    # if any action(evaluation) smaller than min_val, replace it and store the action
    min_val = float("inf")
    possible_move = possible_movements(board, player, positions)

    # A ghost can make no move, and evaluate current state if it doesn't make move
    if len(possible_move)==0: 
        return evaluate(board, positions), " "

    next = random.choice(possible_move)

    # similar with get_max, get minimum action(evaluation) made by player(ghost)
    for move in possible_move:
        # print(player,"checking: ",move)
        tmr_positions = dict()
        for p in positions:
            tmr_positions[p] = positions[p]
        movements = {'N': (-1, 0), 'S': (1, 0), 'W': (0, -1), 'E': (0, 1)}
        # update tmr_positions (current player makes the move)
        row, col = tmr_positions[player]
        r, c = movements[move]
        tmr_positions[player] = [row+r, col+c]

        # store next players in a dictionary
        next_player = {"P": "W"}
        ghosts = [g for g in positions if g!="P"]
        for i in range(len(ghosts)-1):
            next_player[ghosts[i]] = ghosts[i+1]

        if player not in next_player: # meaning that next player is pacman, so use maxi function
            if depth == k:
                # terminal state
                tmr_max = evaluate(board, tmr_positions)

            else:
                tmr_max = get_max(board, "P", tmr_positions, depth+1)
        else:
            tmr_max = get_min(board, next_player[player], tmr_positions, depth)[0]
        if util:
            tmr_max += 500
        if tmr_max <= min_val:
            min_val = tmr_max
            next = move

    return min_val, next

def next_move(board, player, positions):
    
    ghosts = [p for p in positions if p!="P"]
    # print("-----------------MINIMAX-----------------")
    if player == "P":
        # pacman plays as max agent
        next = get_max(board, "P", positions, 1)
    else:
        # other players play as min agents

        # $$$$$$$$$$$$$ Ghost Minimax $$$$$$$$$$$$$$$$$
        mm = get_min(board, player, positions, 1)
        next = mm[1]
        # if no possible move can be made, just continue to next turn (only for ghost)
        if next==" ":
            # print("-----------------RESULT-----------------")
            # print(player, ":", next)
            copy = makeboard(board,positions)
            # print("\n".join(copy))
            return next, "\n".join(makeboard(board, positions))
        # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

        # $$$$$$$$$$$$$$$$$$$$ New $$$$$$$$$$$$$$$$$$$$$
        # $$$$$$$$$$$$ Ghost Randomly Move $$$$$$$$$$$$$
        # possible = possible_movements(board, player, positions)
        # if len(possible)==0:
        #     copy = makeboard(board, positions)
        #     return " ", "\n".join(copy)
        # next = random.choice(possible)
        # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$


    # update position for player
    movements = {'N': (-1, 0), 'S': (1, 0), 'W': (0, -1), 'E': (0, 1)}
    row, col = positions[player] # old position
    r, c = movements[next]
    row, col = row+r, col+c 
    positions[player] = [row, col]

    # pacman eats food, change the board
    if player=="P":
        if board[row][col] == ".":
            board[row] = board[row][:col]+" "+board[row][col+1:]

    # print("-----------------RESULT-----------------")
    # print(player, ":", next)
    copy = makeboard(board,positions)
    # print("\n".join(copy))

    return next, "\n".join(copy)

def possible_movements(board, player, positions):
    movements = {'N': (-1, 0), 'S': (1, 0), 'W': (0, -1), 'E': (0, 1)}
    ghosts = [p for p in positions if p!="P"]
    ghost_positions = [positions[g] for g in positions if g != "P"]
    row, col = positions[player]
    possible = tuple()
    if player in ghosts:
        for move in sorted(movements):
            r, c = movements[move]
            if board[row+r][col+c] != "%" and [row+r, col+c] not in ghost_positions:
                possible += tuple(move)
    else:
        for move in sorted(movements):
            r,c = movements[move]
            if board[row+r][col+c] != "%":
                possible += tuple(move)
    return possible

def makeboard(board, positions):
    # used to make a board with players shown on the board, do not change orgininal board
    copy = [row[:] for row in board]
    for pp in positions:
        row, col = positions[pp]
        copy[row] = copy[row][:col]+pp+copy[row][col+1:]
    return copy

def check_end(board, player, positions):
    # used to check if game over, only used in main function
    global score, nn
    # if all food eaten -> P wins
    if player == "P":
        score -= 1
        n = sum([r.count(".") for r in board])
        # update score if any food is eaten
        if n < nn: 
            score += 10*(nn-n)
            nn = n
        # if number of food on the board is 0, finish game
        if nn == 0:
            score += 500
            return "P"
    # if P eaten -> ghost wins
    ghost_positions = [positions[player] for player in positions if player != "P"]
    if positions["P"] in ghost_positions:
        score -= 500
        return "Ghost"

    return False

def evaluate(board, positions):
    # evaluation function
    # calculate distance to ghost and distance to foods (closer ghost/food has higher correlation)
    # number of ghost/number of walls and number of foods are also considered


    p_row, p_col = positions["P"] # pacman
    ghosts = [g for g in positions if g!="P"]
    g_row, g_col = dict(), dict()
    for gh in ghosts:
        g_row[gh], g_col[gh] = positions[gh]
    distances = dict()
    die = False
    for gg in ghosts:
        distances[gg] = abs(p_row-g_row[gg])+abs(p_col-g_col[gg])
        if distances[gg] == 0:
            die = True
    if die:
        # if pacman died, no need to evaluate
        return float("-inf")
    minimum = min([distances[g] for g in distances])
    dd = minimum
    while len(distances) > 1:
        # closer ghost has higher weight
        for gg in distances:
            if distances[gg] == minimum:
                del distances[gg]
                break
        minimum = min([distances[g] for g in distances])
        if len(distances) > 0:
            dd = dd*0.6+minimum*0.4
    distance_between_players = dd

    foods = []
    for i in range(len(board)):
        foods += [(i,j) for j in range(len(board[i])) if board[i][j] == '.']
    d = [(abs(p_row-food[0])+abs(p_col-food[1])) for food in foods] # distance between food
    num_of_food = sum([row.count(".") for row in board])

    if num_of_food == 0:
        return float("inf")

    minimum = min(d)
    s = minimum
    while len(d) > 1 and len(d) > num_of_food-10:
        # only care for nearby food
        # closer food has higher weight
        d.remove(minimum)
        minimum = min(d)
        s = s*0.8+minimum*0.2
    distance_between_food = 1/(s+0.5) # smaller distance means higher preference
    num_of_boundaries = sum([row.count("%") for row in board])
    a = (len(board)*len(board[0])) / num_of_boundaries # more boundaries, smaller a

    b = math.sqrt(len(board)**2+len(board[0])**2) / (num_of_food ** 0.5)
    total = a*distance_between_players + b*distance_between_food*1000 
    # 1000 used to make food more important than ghost, so that end some infinite loop
    
    return total

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])    
    problem_id = 5
    file_name_problem = str(test_case_id)+'.prob' 
    file_name_sol = str(test_case_id)+'.sol'
    path = os.path.join('test_cases','p'+str(problem_id)) 
    problem = parse.read_layout_problem(os.path.join(path,file_name_problem))
    k = int(sys.argv[2])
    num_trials = int(sys.argv[3])
    verbose = bool(int(sys.argv[4]))
    print('test_case_id:',test_case_id)
    print('k:',k)
    print('num_trials:',num_trials)
    print('verbose:',verbose)
    start = time.time()
    win_count = 0
    for i in range(num_trials):
        solution, winner = min_max_mulitple_ghosts(copy.deepcopy(problem), k)
        if winner == 'Pacman':
            win_count += 1
        if verbose:
            print(solution)
    win_p = win_count/num_trials * 100
    end = time.time()
    print('time: ',end - start)
    print('win %',win_p)