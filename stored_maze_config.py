#PART OF VERSION 4.0
# The Import of "random" is being used to generate random maze size
import random

###############################################
# GENERAL CONFIGS
# Delaying building drawn maze (Press Enter to start building Maze if set to True)
f = open("configs/general/delay_maze_build.txt", "r")
content = f.readline()
f.close() 
if content == "True":
    delay = True
else: 
    delay = False

# Print drawn grid in console
f = open("configs/general/console_print_grid.txt", "r")
content = f.readline()
f.close() 
if content == "True":
    print_grid = True
else: print_grid = False

# Using Pledge Alogrithm
pledge = True


# Save a screenshot of the solved maze (Turned on by default if multisolving is turned on)
f = open("configs/general/take_solution_screenshot.txt", "r")
content = f.readline()
f.close() 
if content == "True":
    take_solution_screenshot = True
else: take_solution_screenshot = False

###############################################
# MAZE SIZE CONFIGS
# Using a random maze size (If this is set equal to True, the maze_size config is irrelevant)
f = open("configs/maze_size/random_maze_size.txt", "r")
content = f.readline()
f.close() 
if content == "True":
    random_maze_size = True
else: random_maze_size = False

# Set Maximum Maze Size (Recommended to keep this at 70 or below)
f = open("configs/maze_size/max_size.txt", "r")
content = f.readline()
f.close()
content = int(content)
max = content

# maze height and width (min 10 / max 70)
f = open("configs/maze_size/custom_maze_size.txt", "r")
content = f.readline()
f.close()
maze_size = int(content)

f = open("configs/maze_size/min_maze_size.txt", "r")
content = f.readline()
f.close()
min_maze_size = int(content)
if min_maze_size < 15:
    min_maze_size = 15

f = open("configs/maze_size/max_maze_size.txt", "r")
content = f.readline()
f.close()
max_maze_size = int(content)

if random_maze_size == True:
    maze_size = random.randint(min_maze_size, max_maze_size)
    f = open("configs/maze_size/custom_maze_size.txt", "w")
    f.write(str(maze_size))
    f.close()


maze_height = maze_size
maze_width = maze_size

###############################################
# CONTROL IN MAIN CODE
# CELL DIMENSION CONFIGS
shapesize = 1


if maze_size < 10:
    maze_size = 10
if maze_size >= 10 and maze_size <= 35:
    shapesize = 1
if maze_size > 35:
    shapesize = 0.5

# If maze size bigger than maximum, set it equal to maximum
if maze_size >= max:
    maze_size = max
    shapesize = 0.5

###############################################
# COLOR CONFIGS (Defaults: Wall = "white", Solutionpath = "green", Visited Cells = "red")

# Basic Wall = (255,255,255), Solutionpath = (0,255,0), Visited = (255,0,0), Turtle = (0,0,255)

f = open("configs/color/wall.txt", "r")
content = f.readline()
f.close()
content = content[1:-1]
content = content.replace(" ", "")
content = content.split(",")
wall_color = ((int(content[0]), int(content[1]), int(content[2])))

f = open("configs/color/solutionpath.txt", "r")
content = f.readline()
f.close()
content = content[1:-1]
content = content.replace(" ", "")
content = content.split(",")
solutionpath_color = ((int(content[0]), int(content[1]), int(content[2])))


f = open("configs/color/visitedcells.txt", "r")
content = f.readline()
f.close()
content = content[1:-1] 
content = content.replace(" ", "")
content = content.split(",")
visitedcells_color = ((int(content[0]), int(content[1]), int(content[2])))

# Turtle Color setting can be found at "TURTLE CONFIGS"

###############################################
# SOLVE STEP BY STEP CONFIG (By pressing "ENTER"/"RETURN" after each step)
f = open("configs/general/step_by_step.txt", "r")
content = f.readline()
f.close() 
if content == "True":
    stepbystep = True
else: stepbystep = False

###############################################
# PATH CONFIGS
# Print Path Calculations to Console
f = open("configs/path/print_calculations.txt", "r")
content = f.readline()
f.close() 
if content == "True":
    print_path_calculations = True
else: print_path_calculations = False

# Print Path Calculations to the Logfile
f = open("configs/path/log_calculations.txt", "r")
content = f.readline()
f.close() 
if content == "True":
    log_path_calculations = True
else: log_path_calculations = False

# Print Path to Console
f = open("configs/path/print_path.txt", "r")
content = f.readline()
f.close() 
if content == "True":
    print_path = True
else: print_path = False


# Show visited cells
f = open("configs/path/show_visited_cells.txt", "r")
content = f.readline()
f.close() 
if content == "True":
    show_visited_cells = True
else: show_visited_cells = False

f = open("configs/path/draw_while_solving.txt", "r")
content = f.readline()
f.close() 
if content == "True":
    draw_while_solving = True
else: draw_while_solving = False

#|#|#|#|#|#|#|#|#|#|#|#|#|#|#|#|
# CONTROL IN MAIN CODE
# Don't change this (It deactivates everything related to the visited cells, if they are disabled...)
if show_visited_cells == False:
    draw_while_solving = False
#|#|#|#|#|#|#|#|#|#|#|#|#|#|#|#|    

###############################################
# TURTLE CONFIGS (Defaults: Shape = "turtle", Color = "blue")
turtle_shape = "turtle"


f = open("configs/color/turtle.txt", "r")
content = f.readline()
f.close() 
content = content[1:-1] 
content = content.replace(" ", "")
content = content.split(",")
turtle_color = ((int(content[0]), int(content[1]), int(content[2])))

###############################################
# SPEED CONFIGS
# Drawingspeed 0 = Default Turtle Speed, the higher the number the faster the maze is being built...
f = open("configs/speed/maze_drawing.txt", "r")
content = f.readline()
f.close() 
maze_drawing_speed = int(content)

# Time the Turtle takes per step (in seconds) (Set equal to zero for maximum speed)
f = open("configs/speed/maze_solving.txt", "r")
content = f.readline()
f.close() 
maze_solving_speed = int(content)

# 
f = open("configs/speed/turtle.txt", "r")
content = f.readline()
f.close() 
turtle_speed = int(content)

# Time between each solution cell being drawn... (in seconds) (Set equal to zero for maximum speed)
f = open("configs/speed/solution_drawing.txt", "r")
content = f.readline()
f.close() 
solution_drawing_speed = int(content)

###############################################
# MULTISOLVE CONFIGS
solve_multiple_mazes = False
auto_solve_multiple_mazes = False
# Solve multiple mazes in a row (manually)
f = open("configs/multisolve/manual.txt", "r")
content = f.readline()
f.close() 
if content == "True":
    solve_multiple_mazes = True
else: solve_multiple_mazes = False

# Automatically solve multiple mazes in a row
f = open("configs/multisolve/auto.txt", "r")
content = f.readline()
f.close() 
if content == "True":
    auto_solve_multiple_mazes = True
else: auto_solve_multiple_mazes = False


# Set the amount of mazes you want to be solved
f = open("configs/multisolve/amount.txt", "r")
content = f.readline()
f.close() 
maze_amount = int(content)
###############################################