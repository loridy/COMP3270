def read_grid_mdp_problem_p1(file_path):
    #Your p1 code here
    problem = dict()
    with open(file_path) as file:
        lines = file.read().split("\n")
    problem["seed"] = int(lines[0].split(": ")[1])
    problem["noise"] = float(lines[1].split(": ")[1])
    problem["livingReward"] = float(lines[2].split(": ")[1])
    problem["grid"] = [line.split() for line in lines[4:lines.index("policy:")]]
    problem["policy"] = [line.split() for line in lines[lines.index("policy:")+1:]]
    
    return problem

def read_grid_mdp_problem_p2(file_path):
    #Your p2 code here
    problem = ''
    return problem

def read_grid_mdp_problem_p3(file_path):
    #Your p3 code here
    problem = ''
    return problem