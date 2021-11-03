import os
script_dir = os.path.dirname(__file__) # give the absolute file path to the open() function

def read_grid(filename):
    filename = os.path.join(script_dir, filename)
    f = open(filename,"r", encoding="utf-8")
    lines = f.readlines()

    lines[0] = lines[0].split(" ")
    x,y = int(lines[0][0]), int(lines[0][1])
    

    grid=[[] for i in range(x)]
    
    for line in lines[2:2+y]:
        for i in range(x):
            grid[i].append(int(line.split(" ")[i]))

    return grid

def read_houses(filename):
    filename = os.path.join(script_dir, filename)
    f = open(filename,"r", encoding="utf-8")
    lines = f.readlines()

    lines[0] = lines[0].split(" ")
    x,y = int(lines[0][0]), int(lines[0][1])
    nb_houses = int(lines[0][2])

    houses=[[] for i in range(nb_houses)]
    
    for line_nb, line in enumerate(lines[3+y:3+2*y]):
        line = line.split(" ")
        for i in range(x):
            houses[int(line[i])].append((i,line_nb))
    return houses