import sys, parse
from turtle import pos
import time, os, copy
import random, math
score = 0

def better_play_single_ghosts(problem):
    #Your p2 code here
    winner = 'Ghost' # set winner to Ghost originally

    global score
    seed, board = problem["seed"], problem["board"]
    # random.seed(seed, version=1)
    random.seed()
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
            winner = "Pacman"
            break
        if end== "W":
            solution.append("WIN: Ghost")
            break
        # if turn == 100:
        #     break
    return "\n".join(solution), winner

def next_move(board, player, positions):
    global score
    # get all possible movements and randomly make a move
    player_position = positions[player]
    row, col = player_position[0], player_position[1]

    # change original board
    if player=="P" or (player=="W" and board[row][col] != "."):
        # change state to " " if Pacman makes the move or ghost not standing on food
        board[row] = board[row][:col]+" "+board[row][col+1:] 

    # randomly select action
    movements = {'N': (-1, 0), 'S': (1, 0), 'W': (0, -1), 'E': (0, 1)}
    
    possible_move = tuple()
    for move in sorted(movements):
        a, b = movements[move]
        if board[row+a][col+b] != "%":
            possible_move += tuple(move)
    if player == "W":
        next = random.choice(possible_move) # next refers to the movement direction
    else:
        next = evaluation(board, positions, movements, possible_move)
        

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
    # print(copy_board)
    return next, copy_board

def evaluation(board, positions, movements, possible_move):
    foods = []
    for i in range(len(board)):
        foods += [(i,j) for j in range(len(board[i])) if board[i][j] == '.']
    p_row, p_col = positions["P"]
    g_row, g_col = positions["W"]
    evaluation = dict()
    for move in possible_move:
        row, col = p_row+movements[move][0] , p_col+movements[move][1]
        # distance_between_players = math.sqrt((row-g_row)**2+(col-g_col)**2)
        distance_between_players = abs(row-g_row)+abs(col-g_col)
        # in previous question, we allow Pacman move to ghost(suiside)
        # this time, remove such possible move
        if distance_between_players == 0:
            continue
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
        if a > 2: # if number of boundaries more than empty states, then food has higher preference
            b = (len(board)**2+len(board[0])**2) / (num_of_food**0.5)
        else: # else, distance to both should be considered almost equally important
            b = math.sqrt(len(board)**2+len(board[0])**2) / (num_of_food ** 0.5) # more food, smaller b
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
    if positions["W"] == positions["P"]:
        score -= 500
        return "W"
    return False


if __name__ == "__main__":
    test_case_id = int(sys.argv[1])    
    problem_id = 2
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
        solution, winner = better_play_single_ghosts(copy.deepcopy(problem))
        if winner == 'Pacman':
            win_count += 1
        if verbose:
            print(solution)
    win_p = win_count/num_trials * 100
    end = time.time()
    print('time: ',end - start)
    print('win %',win_p)