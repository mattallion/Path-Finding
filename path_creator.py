import random


def create_rows(num_grids, max_size):                 #create random number of rows for desired num. of grids
    m_list = []
    for g in range(num_grids):
        m_list.append(random.randint(8, max_size))
    return m_list


def create_cols(num_grids, max_size):                 #create random number of cols for desired num. of grids
    n_list = []
    for g in range(num_grids):
        n_list.append(random.randint(8, max_size))
    return n_list


def create_grid(m, n):                #fill in a grid with "X", "S", "G", and "_" values
    grid = [["" for col in range(n)] for row in range(m)]
    for col in range(n):                    #create grid boundary of top and bottom walls ("X" values)
        grid[0][col] = "X"
        grid[m-1][col] = "X"
    for row in range(1, m):                  #create grid boundary of side walls ("X" values)
        grid[row][0] = "X"
        grid[row][n-1] = "X"

    start_row = random.randint(1, m-2)       #set the starting position ("S" value)
    start_col = random.randint(1, n-2)
    grid[start_row][start_col] = "S"

    while True:                             #set the goal position ("G" value)
        goal_row = random.randint(1, m-2)
        goal_col = random.randint(1, n-2)
        if grid[goal_row][goal_col] != "S":
            grid[goal_row][goal_col] = "G"
            break

    for row in range(1, m-1):                #set inner obstacles ("X" value)
        for col in range(1, n-1):
            if grid[row][col] == "G" or grid[row][col] == "S":
                continue
            else:
                place_x = random.randint(1,100)
                if place_x < 20:
                    grid[row][col] = "X"
                else:
                    grid[row][col] = "_"
    return grid


def write_files():
    num_grids = int(input("How many grids would you like to create: "))
    max_size = min(max(int(input("Max number of rows/columns (between 8 and 1024): ")), 8), 1024)
    m_list = create_rows(num_grids, max_size)
    n_list = create_cols(num_grids, max_size)
    file = open("pathfinding_a.txt", "w+")
    for g in range(num_grids):
        grid = create_grid(m_list[g], n_list[g])
        for row in range(m_list[g]):
            for col in range(n_list[g]):
                file.write(grid[row][col])
                if col == n_list[g] - 1:
                    file.write("\n")
        file.write("\n")
    file.close()
    print("pathfinding_a.txt file created.")

    num_grids = int(input("How many grids would you like to create: "))
    max_size = min(max(int(input("Max number of rows/columns (between 8 and 1024): ")), 8), 1024)
    m_list = create_rows(num_grids, max_size)
    n_list = create_cols(num_grids, max_size)
    file = open("pathfinding_b.txt", "w+")
    for g in range(num_grids):
        grid = create_grid(m_list[g], n_list[g])
        for row in range(m_list[g]):
            for col in range(n_list[g]):
                file.write(grid[row][col])
                if col == n_list[g] - 1:
                    file.write("\n")
        file.write("\n")
    file.close()
    print("pathfinding_b.txt file created.")