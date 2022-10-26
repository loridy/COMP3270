import sys, parse
import time, os, copy
import random, math
score = 0

def better_play_mulitple_ghosts(problem):
    #Your p4 code here
    winner = "Ghost"
    global score
    seed, board = problem["seed"], problem["board"]
    # random.seed(seed, version=1)
    random.seed()
    # add position of existed players, and delete other players
    tmr = {"P": [], "W": [], "X": [], "Y": [], "Z": []}
    positions = dict()    
    for player in tmr:
        position = [[i, board[i].index(player)] for i in range(len(board)) if player in board[i]]
        if len(position) != 0:
            positions[player] = position[0]

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
    solution.append("\n".join(board))
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
    global score
    # get all possible movements and randomly make a move
    player_position = positions[player]
    row, col = player_position
    ghost_position = [positions[ghost] for ghost in positions if ghost != "P"]
    ghosts = [player for player in positions if player != "P"]

    # change original board
    if player=="P" or (player in ghosts and board[row][col] != "."):
        # change state to " " if Pacman makes the move or ghost not standing on food
        board[row] = board[row][:col]+" "+board[row][col+1:] 

    movements = {'N': (-1, 0), 'S': (1, 0), 'W': (0, -1), 'E': (0, 1)}
    possible_move = tuple()
    # Pacman moves to any direction if not wall
    if player == "P":
        for move in sorted(movements):
            a, b = movements[move]
            if board[row+a][col+b] != "%":
                possible_move += tuple(move)
    # ghost moves to any direction if not wall or other ghosts
    if player in ghosts:
        for move in sorted(movements):
            a, b = movements[move]
            if board[row+a][col+b] != "%" and [row+a, col+b] not in ghost_position:
                possible_move += tuple(move)

    # if there's no movement a ghost can make, return empty move
    if len(possible_move) == 0:
        copy = board[:]
        for key, value in positions.items():
            if key != "P":
                ghost, ghost_row, ghost_col = key, value[0], value[1]
                copy[ghost_row] = copy[ghost_row][:ghost_col] + key + copy[ghost_row][ghost_col+1:]
        copy_board = "\n".join(copy)
        print(copy_board)
        return "" , copy_board
    if player in ghosts:
        next = random.choice(possible_move) # next refers to the movement direction
    else:
        next = evaluate(board, positions, movements, possible_move, ghosts)
    row, col = row+movements[next][0], col+movements[next][1] # position after move

    # update positions:
    positions[player] = [row, col]
    # if player is Pacman, change the board
    if player == "P":
        score -= 1
        # if Pacman makes the move and eats a food, score += 10
        if board[row][col] == ".":
            score += 10
            board[row] = board[row][:col]+"P"+board[row][col+1:]
        # if Pacman meets ghost, change the display to ghost
        elif [row, col] in ghost_position:
            # get ghost name who eats Pacman
            for key, value in positions.items():
                if [row, col] == value and key != "P":
                    ghost = key
                    break
            board[row] = board[row][:col]+ghost+board[row][col+1:] # replace Pacman with the ghost 
        else:
            board[row] = board[row][:col]+"P"+board[row][col+1:]

    # display the copy of the board, with ghost replacing food if they're at the same position, but not changing board
    copy = board[:]
    for key, value in positions.items():
        if key != "P":
            ghost, ghost_row, ghost_col = key, value[0], value[1]
            copy[ghost_row] = copy[ghost_row][:ghost_col] + key + copy[ghost_row][ghost_col+1:]
    copy_board = "\n".join(copy)
    print(copy_board)
    return next, copy_board

def evaluate(board, positions, movements, possible_move, ghosts):
    foods = []
    for i in range(len(board)):
        foods += [(i,j) for j in range(len(board[i])) if board[i][j] == '.']
    p_row, p_col = positions["P"]
    g_row, g_col = dict(), dict()
    for player in ghosts:
        g_row[player], g_col[player] = positions[player]
    evaluation = dict()
    distances = dict()
    print("Selecting: --------------------------------------")
    for move in possible_move:
        print("move to:", move)
        row, col = p_row+movements[move][0] , p_col+movements[move][1]
        skip = False
        for ghost in ghosts:
            # distances[ghost] = math.sqrt((row-g_row[ghost])**2+(col-g_col[ghost])**2)
            distances[ghost] = abs(row-g_row[ghost])+abs(col-g_col[ghost])

            if distances[ghost] == 0:
                skip = True
        if skip:
            continue
        
        minimum = min([distances[ghost] for ghost in distances])
        while len(distances) > 1:
            minimum = min([distances[ghost] for ghost in distances])
            for ghost in distances:
                if distances[ghost] == minimum:
                    del distances[ghost]
                    break

            # num_of_min = sum([1 for ghost in distances if distances[ghost]==minimum])
            if len(distances) > 0:
                minimum = minimum*0.6+min([distances[ghost] for ghost in distances])*0.4

        print(distances)
        print("before:",minimum)
        # distance_between_players = sum([distances[ghost]*0.6/num_of_min if distances[ghost]==minimum else distances[ghost]*0.4/(len(distances)-num_of_min) for ghost in distances])
        distance_between_players = minimum
        # n = [distances[ghost]*0.8/num_of_min if distances[ghost]==minimum else distances[ghost]*0.2/(len(distances)-num_of_min) for ghost in distances]
        print("after:", distance_between_players)
        # d = [math.sqrt((row-food[0])**2+(col-food[1])**2+1) for food in foods]
        d = [abs(row-food[0])+abs(col-food[1]) for food in foods]
        distance_between_food = 1/(min(d)+0.5) # smaller distance means higher preference

        # the evaluation function considers number of boundaries, (more boundaries means the distance is actually greater)
        # number of food remained, (more food means you have more options, so don't rely on food)
        # and a constant factor to make evaluation function for food 
        # for number_of_boundaries, if more boundaries on the board, the function should rely less on distance_between_players
        # for number_of_food, the function rely more on food if number of food remained is smaller
        num_of_boundaries = sum([row.count("%") for row in board])
        num_of_food = len(d)
        a = (len(board)*len(board[0])) / num_of_boundaries # more boundaries, smaller a
        if a > 2:
            b = (len(board)**2+len(board[0])**2) / (num_of_food ** 0.5)
        else:
            b = math.sqrt(len(board)**2+len(board[0])**2) / (num_of_food ** 0.5) # more food, smaller b
        print("evaluation function: ")
        print(a,"*", distance_between_players,"+", b, "*", distance_between_food,"=", (a*distance_between_players+b*distance_between_food))
        evaluation[a*distance_between_players+b*distance_between_food] = move
    if len(evaluation)==0:
        return random.choice(possible_move)
    return evaluation[max(evaluation)]


def check_end(board, player, positions):
    global score
    # if all food eaten -> P wins
    if player == "P":
        food = sum([line.count(".") for line in board])
        if food == 0:
            score += 500
            return "P"
    # if P eaten -> ghost wins
    ghost_positions = [positions[player] for player in positions if player != "P"]
    if positions["P"] in ghost_positions:
        score -= 500
        return "Ghost"

    return False

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
            pass
            # print(solution)
    win_p = win_count/num_trials * 100
    end = time.time()
    print('time: ',end - start)
    print('win %',win_p)