import sys, random, grader, parse
score = 0

def random_play_single_ghost(problem):
    #Your p1 code here
    global score
    seed, board = problem["seed"], problem["board"]
    random.seed(seed, version=1)
    positions = dict()
    positions["P"] = [[i, board[i].index("P")] for i in range(len(board)) if "P" in board[i]][0]
    positions["W"] = [[i, board[i].index("W")] for i in range(len(board)) if "W" in board[i]][0]
    players={0: "P", 1:"W"}
    turn, score = 0, 0
    solution = []

    # GAME STARTS
    solution.append(f"seed: {seed}")
    solution.append(str(turn))
    solution.append("\n".join(board))
    while True:
        turn += 1
        next = next_move(board, players[(turn-1)%2], positions)
        solution.append(f"{turn}: {players[(turn-1)%2]} moving {next[0]}")
        solution.append(next[1])
        end = check_end(board, players[(turn-1)%2], positions)
        solution.append(f"score: {score}")
        if end=="P":
            solution.append("WIN: Pacman")
            break
        if end== "W":
            solution.append("WIN: Ghost")
            break

    return "\n".join(solution)

def next_move(board, player, positions):
    global score
    # get all possible movements and randomly make a move
    player_position = positions[player]
    row, col = player_position[0], player_position[1]

    # change original board
    if player=="P" or (player=="W" and board[row][col] != "."):
        # change state to " " if Pacman makes the move or ghost not standing on food
        board[row] = board[row][:col]+" "+board[row][col+1:] 


    movements = {'N': (-1, 0), 'S': (1, 0), 'W': (0, -1), 'E': (0, 1)}
    possible_move = tuple()
    for move in sorted(movements):
        a, b = movements[move]
        if board[row+a][col+b] != "%":
            possible_move += tuple(move)
    next = random.choice(possible_move) # next refers to the movement direction
    row, col = row+movements[next][0], col+movements[next][1] # position after move

    # update positions:
    positions[player] = [row, col]
    if player == "P":
        score -= 1
        # if Pacman makes the move and eats a food, score += 10
        if board[row][col] == ".":
            score += 10
            board[row] = board[row][:col]+"P"+board[row][col+1:]
        # if Pacman meets ghost, replace Pacman with ghost
        elif [row, col] == positions["W"]:
            board[row] = board[row][:col]+"W"+board[row][col+1:]
        else:
            board[row] = board[row][:col]+"P"+board[row][col+1:]

    # display the copy of the board, with ghost replacing food if they're at the same position, but don't change board
    copy = board[:]
    w_row, w_col = positions["W"][0], positions["W"][1]
    copy[w_row] = copy[w_row][:w_col] + "W" + copy[w_row][w_col+1:]
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
    if positions["W"] == positions["P"]:
        score -= 500
        return "W"
    return False

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 1
    grader.grade(problem_id, test_case_id, random_play_single_ghost, parse.read_layout_problem)