from cmath import exp
import sys, parse
from turtle import pos
import time, os, copy
import random, math
score = 0 # total score
nn = 0 # original number of food
def expecti_max_mulitple_ghosts(problem, k):
    #Your p6 code here
    winner = "Ghost"
    global score, nn
    seed, board = problem["seed"], problem["board"]
    # random.seed(seed, version=1)
    nn = sum([r.count(".") for r in board])
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
        # if turn == 100:
        #     break
    return "\n".join(solution), winner

def get_max(copy_board, player, positions, depth):
    board = [row[:] for row in copy_board]
    num_of_food = sum([row.count(".") for row in board])
    # if no food on the board, get positive infinite utility
    if num_of_food == 0: 
        return float("inf")
    g_positions = [positions[g] for g in positions if g!="P"]
    # if pacman on ghosts' location, meanning that it's eaten, so get negative infinite utility
    if positions["P"] in g_positions: 
        return float("-inf") 

    pr,pc = positions["P"]
    if board[pr][pc] == ".":
        board[pr] = board[pc][:pc]+" "+board[pr][pc+1:]

    max_val = float("-inf")
    possible = possible_movements(board, player, positions) 
    next = random.choice(possible)
    for move in possible:
        tmr_positions = dict()
        for p in positions:
            tmr_positions[p] = positions[p]
        movements = {'N': (-1, 0), 'S': (1, 0), 'W': (0, -1), 'E': (0, 1)}
        # update tmr_positions for the next player
        row, col = tmr_positions[player]
        r, c = movements[move]
        tmr_positions[player] = [row+r, col+c]
        tmr_next = expectimax(board, "W", tmr_positions, depth)
        if tmr_next >= max_val:
            max_val = tmr_next
            next = move
        
    if depth > 1:
        return max_val
    return next

def expectimax(copy_board, player, positions, depth):
    # util represents if previous player eats a food (specifically for pacman)
    util = False 
    board = [row[:] for row in copy_board]
    pr,pc = positions["P"]
    if board[pr][pc] == ".":
        # check last action made by pacman: if it eats a food; if so, change util to True
        board[pr] = board[pr][:pc]+" "+board[pr][pc+1:]
        util = True 
    num_of_food = sum([row.count(".") for row in board])
    # same with get_max: check if game over
    if num_of_food == 0:
        return float("inf")
    g_positions = [positions[g] for g in positions if g!="P"]
    if positions["P"] in g_positions:
        # print("die")
        return float("-inf")
    

    possible = possible_movements(board, player, positions)
    if len(possible)==0:
        # no move can make, utility be 0
        return 0
    expected_util = 0
    prob = 1/len(possible)
    next_player = {"P": "W"}
    ghosts = [g for g in positions if g!="P"]
    for i in range(len(ghosts)-1):
        next_player[ghosts[i]] = ghosts[i+1]
    for move in possible:
        tmr_positions = dict()
        for p in positions:
            tmr_positions[p] = positions[p]
        movements = {'N': (-1, 0), 'S': (1, 0), 'W': (0, -1), 'E': (0, 1)}
        
        # update tmr_positions (current player makes the move)
        row, col = tmr_positions[player]
        r, c = movements[move]
        tmr_positions[player] = [row+r, col+c]
        if player not in next_player:
            # meaning this is the last ghost, so next player is pacman
            if depth==k:
                # terminal state
                expected_util += prob*evaluate(board, tmr_positions)
            else:
                # pass to pacman
                expected_util += prob*get_max(board, "P", tmr_positions, depth+1)
        else:
            expected_util += prob*expectimax(board, next_player[player], tmr_positions, depth)
    if util:
        expected_util += 500
        # print("hahah")
    return expected_util

def next_move(board, player, positions):
    if player == "P":
        next = get_max(board, player, positions, 1)
    else:
        possible = possible_movements(board, player, positions)
        if len(possible) == 0:
            copy = makeboard(board, positions)
            return " ", "\n".join(copy)
        next = random.choice(possible)

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
    # used to make a board with players shown on the board
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
        if n<nn:
            score += 10*(nn-n)
            nn = n
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
        # print(distances)
        for gg in distances:
            if distances[gg] == minimum:
                del distances[gg]
                break
        minimum = min([distances[g] for g in distances])
        if len(distances) > 0:
            # mm = min([distances[g] for g in distances])
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
        d.remove(minimum)
        minimum = min(d)
        s = s*0.8+minimum*0.2
    distance_between_food = 1/(s+0.5) # smaller distance means higher preference
    # corelation
    num_of_boundaries = sum([row.count("%") for row in board])
    a = (len(board)*len(board[0])) / num_of_boundaries # more boundaries, smaller a
    # if a > 2:
    #     b = (len(board)**2+len(board[0])**2) / (num_of_food ** 0.5)
    # else:
    #     b = math.sqrt(len(board)**2+len(board[0])**2) / (num_of_food ** 0.5) # more food, smaller b
    # b = len(board)**2+len(board[0])**2 / (num_of_food ** 0.5)
    b = math.sqrt(len(board)**2+len(board[0])**2) / (num_of_food ** 0.5)
    total = a*distance_between_players + b*distance_between_food*1000
    
    return total

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])    
    problem_id = 6
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
        solution, winner = expecti_max_mulitple_ghosts(copy.deepcopy(problem), k)
        if winner == 'Pacman':
            win_count += 1
        if verbose:
            print(solution)
    win_p = win_count/num_trials * 100
    end = time.time()
    print('time: ',end - start)
    print('win %',win_p)