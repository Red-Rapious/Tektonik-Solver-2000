# Created by Antoine Groudiev - 2021 (CC BY-SA)

from reader import read_grid, read_houses
from colors import colors
from copy import deepcopy
from time import time

# --- Initial input: grid + houses ---
grid_ref = read_grid("Grids/tektonik4.tkn")
houses = read_houses("Grids/tektonik4.tkn")

# --- Solver ---
# This program uses a backtracking algorithm
# For each box, it checks if a given number is compatible with the rest of the grid
# If it's not, it increment the number; if it is, it recursively calls it for the next box

dico_houses = {} # dynamicly programming the dico_houses function
def which_house(x, y) -> int:
  """ Return the house to which the box x,y belongs """
  if (x,y) in dico_houses.keys():
    return dico_houses[(x,y)]
  else:
    for i in range(len(houses)):
      if (x, y) in houses[i]:
        dico_houses[(x,y)] = i
        return i
  print("Error: box not in any house:", str(x)+ ",", y)
  return -1

def is_compatible(x, y, n) -> bool:
  """ Return if the number in x,y is compatible with the rest of the grid, according to the rules: 
  - each house may contain only once each number
  - each number must be <= to the len of the house
  - two identical numbers can't be adjacents (even in diagonal)
  """
  global grid
  house = which_house(x, y)
  compatible = True
  # rule 2
  if n>len(houses[house]):
    compatible = False

  # rule 1
  for coord in houses[house]:
    if grid[coord[0]][coord[1]] == n and coord!=(x,y):
      compatible = False

  # rule 3
  bx0, bxM = x!=0, x!=len(grid)-1
  by0, byM = y!=0, y!=len(grid[0])-1

  if bx0 and by0 and grid[x-1][y-1] == n:
    compatible = False
  if by0 and grid[x][y-1] == n:
    compatible = False
  if bxM and by0 and grid[x+1][y-1] == n:
    compatible = False
  if bxM and grid[x+1][y] == n:
    compatible = False
  if bxM and byM and grid[x+1][y+1] == n:
    compatible = False
  if byM and grid[x][y+1] == n:
    compatible = False
  if byM and bx0 and grid[x-1][y+1] == n:
    compatible = False
  if bx0 and grid[x-1][y] == n:
    compatible = False

  
  return compatible

def print_grid(grid):
  """ Nicely displays a grid, with color for each house """
  for y in range(len(grid[0])):
    for x in range(len(grid)):
        print("" if x==0 else " ", end="")
        h=which_house(x,y)
        color = colors.color_list[h] if h<len(colors.color_list) else colors.reset
        print(color + str(grid[x][y]), end="")
    print(colors.reset)

count=0 # track the number of calls of the revursive function
def backtracking(x, y, n) -> bool: # return value: bool or the updated grid
  """ Recursive function returning True if the n value in x,y is a the good value in the solution given by the algorithm
      Convention is that if x==-1, it's the initial launch state
  """
  global grid_ref
  global count
  global grid

  count+=1

  is_possible = True

  if grid_ref[x][y] != 0: # if already in the starting grid, it's the good one
    is_possible = True
  elif x!=-1: # if x==-1, we don't need to be sure that the "current" box is compatible, just the ones after
    grid[x][y] = n
    is_possible = is_compatible(x, y, n)
    if not is_possible:
      return False


  if not (x==len(grid)-1 and y==len(grid[0])-1): # if not the last box of the grid
    # next coordinates for the box to backtrack
    next_x = (x+1)%len(grid) # big brain math
    next_y = y+(next_x==0)

    next_is_possible = False
    for i in range(1,len(houses[which_house(next_x, next_y)])+1): # try every possible value possible for the next box
      next_is_possible = backtracking(next_x, next_y, i)
      if next_is_possible:
        break
    if (not next_is_possible) and grid_ref[next_x][next_y] == 0:
      grid[next_x][next_y] = 0
    is_possible = is_possible and next_is_possible

  return is_possible


print("[Event] Starting solving the grid:")
print_grid(grid_ref)
print("")
start_time = time()

# one-box houses must be a 1
for house in houses:
  if len(house) == 1:
    grid_ref[house[0][0]][house[0][1]] = 1

grid = deepcopy(grid_ref)
is_solvable = backtracking(-1, -1, -1) # x=-1 for convention, y=-1 to have y=0 at line 107, n value is unimportant
if not is_solvable:
  print("[Event] This Tektonik can't be solved, even by TektonikSolver2000")
else:
  print("[Event] Grid solved:")
  print_grid(grid)

print("\n[Info] Execution time:", colors.fg.red+str(round(time()-start_time, 1))+colors.reset, "seconds")
print("[Info] Calls of the recursive function:", str(count)) # complexity is something like 5ˆ(l*L)