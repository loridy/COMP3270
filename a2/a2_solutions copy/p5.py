from lzma import CHECK_CRC32
import sys, parse
import time, os, copy
import random, math
score = 0
def makeboard(board, positions):
    copy = [row[:] for row in board]
    # print("@@@@@@@@@@@@@: ", positions)
    for player in positions:
        row, col = positions[player]
        copy[row] = copy[row][:col]+player+copy[row][col+1:]
    return copy

def min_max_mulitple_ghosts(problem, k):
    #Your p5 code here
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

    # clean board
    for i in range(len(players)):
        row, col = positions[players[i]]
        board[row] = board[row][:col]+" "+board[row][col+1:]
    num = len(players)
    turn, score = 0, 0
    solution = []

    # GAME STARTS
    solution.append(f"seed: {seed}")
    solution.append(str(turn))
    solution.append("\n".join(board))
    print("---------- BEFORE MINIMAX ----------")
    copy = makeboard(board, positions)
    print("\n".join(copy))
    turn = 1
    while True:
        next = next_move(board, players[(turn-1)%num], positions)
        solution.append(f"{turn}: {players[(turn-1)%num]} moving {next[0]}")
        solution.append(next[1])
        if next == "Lose":
            solution.append("WIN: Ghost")
            break
        else:
            end = check_end(board, players[(turn-1)%num], positions)
        solution.append(f"score: {score}")
        # print("positions -------> ", positions)
        if end=="P":
            solution.append("WIN: Pacman")
            winner = "Pacman"
            break
        if end == "Ghost":
            solution.append("WIN: Ghost")
            break
        # if turn == 11:
        #     break
        turn += len(players)*k
    return "\n".join(solution), winner

def possible_moves(board, movements, player, ghosts, positions):
    ghost_position = [positions[ghost] for ghost in positions if ghost != "P"]
    player_position = positions[player]
    row, col = player_position
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
    return possible_move

def next_move(board, player, positions):
    steps = 1
    while steps!=0:
        steps -= 1
        global score
        # get all possible movements and randomly make a move
        player_position = positions[player]
        row, col = player_position
        ghost_position = [positions[ghost] for ghost in positions if ghost != "P"]
        ghosts = [player for player in positions if player != "P"]

        movements = {'N': (-1, 0), 'S': (1, 0), 'W': (0, -1), 'E': (0, 1)}
        possible_move = possible_moves(board, movements, player, ghosts, positions)

        # print("---------- RUNNING MINIMAX ----------")
        num_of_food = sum([line.count(".") for line in board])
        step = k
        # print("positions before minimax", positions["P"])
        print(possible_move)
        
        
        
        if player=="P":
            # next = evaluate(board, positions, movements, possible_move, ghosts)
            print("now: ", positions["P"])
            mm = max_value(board, player, positions, movements, possible_move, ghosts, k, num_of_food, step, "")
            print("$$$$$$$$$$$$$$$$", mm[0])
            next, tmr_positions, order = mm[1:] # pacman plays as maximum agents
            print("@@@@@@@@@@@@@@@@@@@@@@@", order)
            print("next pacman: ", next)
        
        
        
        
        # print("positions after minimax",tmr_positions["P"])
        for m in order:
            r, c = positions["P"]
            rr, cc = movements[m]
            if board[r+rr][c+cc] == ".":
                # print("clear food")
                board[r+rr] = board[r+rr][:c+cc]+" "+board[r+rr][c+cc+1:]
                positions["P"] = [r+rr, c+cc]
        if next==" ":
            copy = makeboard(board, positions)
            copy_board = "\n".join(copy)
            print("---------- FINISH MINIMAX ----------")
            print(copy_board)
            return "" , copy_board
        row, col = row+movements[next][0], col+movements[next][1] # position after move

        # update positions:
        # print(row, col)
        positions[player] = tmr_positions["P"]
        # print(tmr_positions["P"])

        # update board only if pacman eats a food
        if player == "P":
            score -= 1
            if board[row][col] == ".":
                score += 10
                board[row] = board[row][:col]+" "+board[row][col+1:]

        copy = makeboard(board, positions)
        copy_board = "\n".join(copy)
        print("---------- Pacman MINIMAX ----------")
        print(copy_board)
        rrr, ccc=positions["P"]
        if board[rrr][ccc] == ".":
            board[rrr] = board[rrr][:ccc]+" "+board[rrr][ccc+1:]

        ghost_positions = [positions[ghost] for ghost in positions if ghost != "P"]
        # print("P: ", tmr_positions["P"])
        # print(ghost_positions)

        if tmr_positions["P"] in ghost_positions:
            return "Lose"

        # after pacman moves, proceed ghosts
        next_player = {"P": "W"}
        for i in range(len(ghosts)):
            if i == len(ghosts)-1:
                next_player[ghosts[i]] = "P"
                break
            next_player[ghosts[i]] = ghosts[i+1]
        # print(next_player)
        player = next_player[player]
        # print(player)
        while (player != "P"):
            # update positions:
            positions[player] = tmr_positions[player]
            # print(player, positions[player])
            copy = makeboard(board, positions)
            # print("positions:", positions)
            copy_board = "\n".join(copy)
            print("----------", player, "MINIMAX ----------")
            print(copy_board)

            player = next_player[player]
            # print(player)
    return next, copy_board

def evaluate(board, positions, movements, possible_move, ghosts):
    foods = []
    for i in range(len(board)):
        foods += [(i,j) for j in range(len(board[i])) if board[i][j] == '.']
    p_row, p_col = positions["P"]
    g_row, g_col = dict(), dict()
    for player in ghosts:
        g_row[player], g_col[player] = positions[player]
    # print(positions["W"])
    evaluation = dict()
    distances = dict()
    # print("Selecting: --------------------------------------")
    for move in possible_move:
        # print("move to:", move)
        row, col = p_row+movements[move][0] , p_col+movements[move][1]
        skip = False
        for ghost in ghosts:
            # distances[ghost] = math.sqrt((row-g_row[ghost])**2+(col-g_col[ghost])**2)
            distances[ghost] = abs(row-g_row[ghost])+abs(col-g_col[ghost])

            if distances[ghost] == 0:
                skip = True
        if skip:
            # print("skip")
            continue
        # minimum = min([distances[ghost] for ghost in distances])
        # num_of_min = sum([1 for ghost in distances if distances[ghost]==minimum])
        # print("distance to ghost:", distances)
        # print("before:",minimum)
        # distance_between_players = sum([distances[ghost]*0.6/num_of_min if distances[ghost]==minimum else distances[ghost]*0.4/(len(distances)-num_of_min) for ghost in distances])
        # n = [distances[ghost]*0.8/num_of_min if distances[ghost]==minimum else distances[ghost]*0.2/(len(distances)-num_of_min) for ghost in distances]
        minimum = min([distances[ghost] for ghost in distances])
        # print("haah")
        while len(distances) > 1:
            minimum = min([distances[ghost] for ghost in distances])
            # print(distances)
            for ghost in distances:
                if distances[ghost] == minimum:
                    del distances[ghost]
                    break
            # print(distances)
            # num_of_min = sum([1 for ghost in distances if distances[ghost]==minimum])
            if len(distances) > 0:
                minimum = minimum*0.6+min([distances[ghost] for ghost in distances])*0.4
        # print("hahah")
        distance_between_players = minimum
        # print(n)
        # print("after:", distance_between_players)
        # d = [math.sqrt((row-food[0])**2+(col-food[1])**2+1) for food in foods]
        d = [abs(row-food[0])+abs(col-food[1]) for food in foods]
        if len(d) != 0:
            distance_between_food = 1/(min(d)+0.5) # smaller distance means higher preference
        else:
            distance_between_food = 1/0.5
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
        # print("evaluation function: ")
        # print(a,"*", distance_between_players,"+", b, "*", distance_between_food,"=", (a*distance_between_players+b*distance_between_food))
        # print(a*distance_between_players+b*distance_between_food)
        evaluation[a*distance_between_players+b*distance_between_food*1000] = move
    if len(evaluation)==0:
        return False
    # update returned value: both max value and corresponding move
    # return (max(evaluation), evaluation[max(evaluation)])
    # print(type(max(evaluation)), max(evaluation))
    if player=="P":
        return max(evaluation)
    else:
        return min(evaluation)
def max_value(board, player, copy_positions, movements, possible_move, ghosts, k, num_of_food, step, o):
    # for pacman, if it eats all food, return current state
    # print("current k is: ", k)
    # print("max: ", player)
    # print(positions["P"])




    positions = dict()
    for key in copy_positions:
        positions[key] = copy_positions[key]
    g_positions = [positions[ghost] for ghost in ghosts]

    if k != 0:
        print(k, ":" )
        print("checking: ",positions["P"],"-----------------")

    # print(k)
    # print("pacman: ", positions["P"])
    # print("ghost: ", g_positions)

    cp_board = [row[:] for row in board]


    # r,c = positions["P"]
    # print("$$$$$$$$$$$$$$$$$$order: ", o)
    # print(o[::-1])
    # for st in o[::-1]:
    #     print(st)
    #     r, c = r-movements[st][0],c-movements[st][1]
    #     print(r,c)
    #     if cp_board[r][c]==".":
    #         cp_board[r] = cp_board[r][:c] + " " + cp_board[r][c+1:]
    #         print("HAAHAHA")
    #         num_of_food -= 1


    if positions["P"] in g_positions: # pacman is eaten
        return float("-inf"), positions["P"], positions, o # negative infinite utility if eaten
    
    if num_of_food==0: # pacman eats all food
        return float("inf"), positions["P"], positions, o # the most utility pacman wants, so it's positive infinite

    if k==0:
        print("find: ", positions["P"])
        u = evaluate(cp_board, positions, movements, possible_move, ghosts)
        # print(possible_move)
        # print("current positions: ", positions["P"], u)



        if board[positions["P"][0]][positions["P"][1]] == ".":
            u += 100
            print("haha")
        return u, positions["P"], positions, o
    max_val = float("-inf")
    tmr = dict()
    for key in positions:
        tmr[key] = positions[key]
    if len(possible_move)==0:
        best_move = " "
    else:
        best_move = random.choice(possible_move)
        tt_row, tt_col = tmr["P"]
        tmr["P"] = [tt_row+movements[best_move][0], tt_col+movements[best_move][1]]
    # print("possible moves: ")
    # print(possible_move)


    p_row, p_col = positions["P"]
    print(best_move, max_val)
    for move in possible_move:
        # print("Pacman checking: ", positions["P"], move)
        row, col = p_row+movements[move][0] , p_col+movements[move][1]
        tmr_num_of_food = num_of_food
        if board[row][col] == ".":
            tmr_num_of_food -= 1
        # ------ make temporary items used for checking recursive value -----

        tmr_positions = dict()
        for key, value in positions.items():
            tmr_positions[key] = value[:]
        tmr_positions["P"] = [row, col]
        # origin_rol, origin_col = positions[player] # renew tmr board with original Pacman moved
        # tmr_board[origin_rol] = tmr_board[origin_rol][:origin_col]+" "+tmr_board[origin_rol][origin_col+1:]
        # tmr_board[row] = tmr_board[row][:col]+player+tmr_board[row][col+1:]
        # checking
        # tmr_board = board[:]

        # print(copy_board)
        # checking end
        # if k==0:

        #     tmr_board = makeboard(board, tmr_positions)

        #     rr, cc = positions['P']
        #     print(tmr_board[rr][cc])
        #     if tmr_board[rr][cc] == ".":
        #         tmr_board[rr] = tmr_board[rr][:cc]+" "+tmr_board[rr][cc+1:]
        #     print(tmr_board[rr][cc])

        

        tmr_possible_move = possible_moves(board, movements, "W", ghosts, tmr_positions)
        # print("tmr_possible_move for W: ", tmr_possible_move)
        ll = min_value(board, "W", tmr_positions, movements, tmr_possible_move, ghosts, k, tmr_num_of_food, step, o)
        
        # print("ll", ll)
        if ll[0] == "eaten":
            # print("eaten")
            return float("-inf"), move, tmr_positions, o # negative infinite utility if eaten
        
        tmr_min_val = ll[0]
        print(move, "tmr_min_val: ", tmr_min_val)
        if tmr_min_val >= max_val:
            print("hah")
            max_val = tmr_min_val
            best_move = move
            tmr = ll[1]
            if type(ll[-1])==str:
                o = ll[-1]
            # return max_val, best_move, tmr, o+best_move
    # !!!! depth matters: waiting for implementation
    # print("---------------------------------------------------")
    # print("current k is ", k)
    # print("---------------------------------------------------")
    # if k == 0:
    #     return max_val
    # print("hahah")
    # return best_move
    print("###############", max_val, best_move)
    return max_val, best_move, tmr, o+best_move

def min_value(board, player, copy_positions, movements, possible_move, ghosts, k, tmr_num_of_food, step, o):
    # print("current k is: ", k)
    # print("min: ", player)
    # for ghost, it it eats pacman, return current utility
    # if check_end(board, player, positions)=="Ghost":
    #     val = float("-inf") # the least utility pacman wants, so it's negative infinite
    #     return val

    positions = dict()
    for key in copy_positions:
        positions[key] = copy_positions[key]
    g_positions = [positions[ghost] for ghost in ghosts]
    if positions["P"] in g_positions:
        return "eaten", positions
    next_ghost = dict()
    for i in range(len(ghosts)-1):
        next_ghost[ghosts[i]] = ghosts[i+1]
    # print(next_ghost)
    min_val = float("inf")
    tmr = dict()
    for key in positions:
        tmr[key] = positions[key]

    if len(possible_move)==0:
        best_move = " "
    else:
        best_move = random.choice(possible_move)
        tt_row, tt_col = tmr[player]
        tmr[player] = [tt_row+movements[best_move][0], tt_col+movements[best_move][1]]

    g_row, g_col = positions[player]
    # check if next player is pacman; if so, plays max, else plays min

    if player not in next_ghost:
        for move in possible_move:
            # print("@@",player, "-------------- CHECKING NEXT MOVE: ", move)
            row, col = g_row+movements[move][0] , g_col+movements[move][1]
            tmr_positions = dict()
            for key, value in positions.items():
                tmr_positions[key] = value[:]
            tmr_positions[player] = [row, col]
            # checking
            # tmr_board = board[:]
            # print("original: ", tmr_board[row])
            # origin_row, origin_col = positions[player] # renew tmr board with original ghost moved
            # tmr_board[origin_row] = tmr_board[origin_row][:origin_col]+" "+tmr_board[origin_row][origin_col+1:]
            # tmr_board[row] = tmr_board[row][:col]+player+tmr_board[row][col+1:]
            tmr_board = makeboard(board, tmr_positions)
            # print("new: ", tmr_board[row])
            # print(copy_board)
            # checking end
            tmr_possible_move = possible_moves(board, movements, "P", ghosts, tmr_positions)
            # print("checking tmr_possible_move for Pacman: ",tmr_possible_move)
            ll = max_value(board, "P", tmr_positions, movements, tmr_possible_move, ghosts, k-1, tmr_num_of_food, step, "")
            tmr_max_val = ll[0]
            if tmr_max_val==False:
                tmr_max_val = float("-inf")
            # print(type(tmr_max_val), type(min_val))
            if tmr_max_val < min_val:
                min_val = tmr_max_val
                best_move = move
                tmr = ll[2]
                if type(ll[-1])==str:
                    o = ll[-1]
            # print(min_val)
    else:
        for move in possible_move:
            # print("@@", player, "-------------- CHECKING NEXT MOVE: ", move)
            row, col = g_row+movements[move][0] , g_col+movements[move][1]
            tmr_positions = dict()
            for key, value in positions.items():
                tmr_positions[key] = value[:]
            tmr_positions[player] = [row, col]
            # checking
            # tmr_board = board[:]
            # origin_row, origin_col = positions[player] # renew tmr board with original ghost moved
            # tmr_board[origin_row] = tmr_board[origin_row][:origin_col]+" "+tmr_board[origin_row][origin_col+1:]
            # tmr_board[row] = tmr_board[row][:col]+player+tmr_board[row][col+1:]
            # print("new: ", tmr_board[row])
            # print(copy_board)
            # checking end
            tmr_possible_move = possible_moves(board, movements, next_ghost[player], ghosts, tmr_positions)
            ll = min_value(board, next_ghost[player], tmr_positions, movements, tmr_possible_move, ghosts, k, tmr_num_of_food, step, o)
            tmr_min_val = ll[0]
            if tmr_min_val == "eaten":
                return float("-inf"), tmr
            if tmr_min_val < min_val:
                min_val = tmr_min_val
                best_move = move
                tmr = ll[1]
            # print(min_val)
    # print(min_val, type(min_val))
    # print(best_move, type(best_move))
    # print(min_val)
    return min_val, tmr, o

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