import sys, parse
from turtle import pos
import time, os, copy
import random, math
score = 0
nn = 0
def better_play_mulitple_ghosts(problem):
    #Your p4 code here
    winner = "Ghost"
    global score, nn
    seed, board = problem["seed"], problem["board"]
    nn = sum([r.count(".") for r in board])
    # random.seed(seed, version=1)
    random.seed()
    # add position of existed players, and delete other players
    tmr = {"P": [], "W": [], "X": [], "Y": [], "Z": []}
    positions = dict()    
    for player in tmr:
        position = [[i, board[i].index(player)] for i in range(len(board)) if player in board[i]]
        if len(position) != 0:
            positions[player] = position[0]

    # clear board
    for player in positions:
        row, col = positions[player]
        board[row] = board[row][:col]+" "+board[row][col+1:]
    # print("\n".join(board))
    copy = makeboard(board, positions)
    # print("\n".join(copy))
    # add players
    players = dict()
    i = 0
    for player in positions:
        players[i] = player
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

def next_move(board, player, positions):
    row, col = positions[player]
    movements = {'N': (-1, 0), 'S': (1, 0), 'W': (0, -1), 'E': (0, 1)}
    possible = possible_movements(board, player, positions)
    if player == "P":
        max_val = float("-inf")
        for move in possible:
            r, c = movements[move]
            tmr_positions = dict()
            for p in positions:
                tmr_positions[p] = positions[p]
            tmr_positions[player] = [row+r, col+c]
            tmr_val = evaluate(board, tmr_positions)
            if tmr_val >= max_val:
                max_val = tmr_val
                next = move
    else:
        if len(possible)==0:
            copy = makeboard(board, positions)
            return " ", "\n".join(copy)
        next = random.choice(possible)

    r, c = movements[next]
    positions[player] = [row+r, col+c]
    if player == "P":
        if board[row+r][col+c] == '.':
            board[row+r] = board[row+r][:col+c]+" "+board[row+r][col+c+1:]
    copy = makeboard(board, positions)
    # print("\n".join(copy))
    return next, "\n".join(copy)


def makeboard(board, positions):
    copy = [row[:] for row in board]
    for player in positions:
        row, col = positions[player]
        copy[row] = copy[row][:col]+player+copy[row][col+1:]
    return copy

def possible_movements(board, player, positions):
    movements = {'N': (-1, 0), 'S': (1, 0), 'W': (0, -1), 'E': (0, 1)}
    ghosts = [player for player in positions if player!="P"]
    ghost_positions = [positions[ghost] for ghost in positions if ghost != "P"]
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

def check_end(board, player, positions):
    global score, nn
    # if all food eaten -> P wins
    if player == "P":
        score -= 1
        n = sum([r.count(".") for r in board])
        if n<nn:
            score += (nn-n)*10
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
    p_row, p_col = positions["P"] # pacman
    ghosts = [ghost for ghost in positions if ghost!="P"]
    g_row, g_col = dict(), dict()
    for ghost in ghosts:
        g_row[ghost], g_col[ghost] = positions[ghost]
    distances = dict()
    die = False
    for ghost in ghosts:
        distances[ghost] = abs(p_row-g_row[ghost])+abs(p_col-g_col[ghost])
        if distances[ghost] == 0:
            die = True
    if die:
        return float("-inf")
    minimum = min([distances[ghost] for ghost in distances])
    while len(distances) > 1:
        minimum = min([distances[ghost] for ghost in distances])
        for ghost in distances:
            if distances[ghost] == minimum:
                del distances[ghost]
                break
        if len(distances) > 0:
            minimum = minimum*0.6+min([distances[ghost] for ghost in distances])*0.4
    distance_between_players = minimum

    foods = []
    for i in range(len(board)):
        foods += [(i,j) for j in range(len(board[i])) if board[i][j] == '.']
    d = [abs(p_row-food[0])+abs(p_col-food[1]) for food in foods] # distance between food
    if len(d) == 0:
        return float("inf")
    distance_between_food = 1/(min(d)+0.5) # smaller distance means higher preference

    # corelation
    num_of_boundaries = sum([row.count("%") for row in board])
    num_of_food = len(d)
    a = (len(board)*len(board[0])) / num_of_boundaries # more boundaries, smaller a
    if a > 2:
        b = (len(board)**2+len(board[0])**2) / (num_of_food ** 0.5)
    else:
        b = math.sqrt(len(board)**2+len(board[0])**2) / (num_of_food ** 0.5) # more food, smaller b
    return a*distance_between_players + b*distance_between_food*10


if __name__ == "__main__":
    test_case_id = int(sys.argv[1])    
    problem_id = 4
    file_name_problem = str(test_case_id)+'.prob' 
    file_name_sol = str(test_case_id)+'.sol'
    path = os.path.join('test_cases','p'+str(problem_id)) 
    problem = parse.read_layout_problem(os.path.join(path,file_name_problem))
    num_trials = int(sys.argv[2])
    verbose = bool(int(sys.argv[3]))
    print('test_case_id:',test_case_id)
    print('num_trials:',num_trials)
    print('verbose:',verbose)
    start = time.time()
    win_count = 0
    for i in range(num_trials):
        solution, winner = better_play_mulitple_ghosts(copy.deepcopy(problem))
        if winner == 'Pacman':
            win_count += 1
        if verbose:
            print(solution)
    win_p = win_count/num_trials * 100
    end = time.time()
    print('time: ',end - start)
    print('win %',win_p)