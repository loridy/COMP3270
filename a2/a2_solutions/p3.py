import sys, grader, parse, math, random
score = 0

def random_play_multiple_ghosts(problem):
    #Your p3 code here
    global score
    seed, board = problem["seed"], problem["board"]
    random.seed(seed, version=1)

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
            break
        if end == "Ghost":
            solution.append("WIN: Ghost")
            break

    return "\n".join(solution)

def next_move(board, player, positions):
    global score
    # get all possible movements and randomly make a move
    player_position = positions[player]
    row, col = player_position
    ghost_position = [positions[ghost] for ghost in positions if ghost != "P"]

    # change original board
    if player=="P" or (player in ["W", "X", "Y", "Z"] and board[row][col] != "."):
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
    if player in ["W", "X", "Y", "Z"]:
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
        return "" , copy_board

    next = random.choice(possible_move) # next refers to the movement direction
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
    return next, copy_board

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
    problem_id = 3
    grader.grade(problem_id, test_case_id, random_play_multiple_ghosts, parse.read_layout_problem)