import path_creator


def find_m_values(filename):
    # Finds m values (# of rows) in each grid contained in file
    # Returns m values in an array
    m_list = []
    file = open(filename, "r+")
    m = 0
    while True:
        line = file.readline()
        if line.strip():
            # Increment m when current line is not empty
            m = m + 1
        else:
            # When line is empty, check next line
            m_list.append(m)
            x = file.tell()
            next_line = file.readline()
            if not next_line.strip():
                # Close file on two consecutive empty lines
                file.close()
                break
            else:
                m = 0
                file.seek(x)
                continue
    return m_list


def find_n_values(filename):
    # Finds n values (# of columns) in each grid contained in file
    # Returns n values in an array (order corresponds to m values array)
    n_list = []
    file = open(filename, "r+")
    while True:
        line = file.readline()
        if line.strip():
            n = len(line) - 1
        else:
            n_list.append(n)
            x = file.tell()
            next_line = file.readline()
            if not next_line.strip():
                file.close()
                break
            else:
                file.seek(x)
                continue
    return n_list


def convert_and_searches(filename, m_list, n_list, output_file):
    # Converts grids to 2D arrays
    file = open(filename, "r+")
    for g in range(len(m_list)):
        grid = [["" for col in range(n_list[g])] for row in range(m_list[g])]
        for row in range(m_list[g]):
            line = file.readline()
            col = 0
            for ch in line:
                if col == n_list[g]:
                    if row == m_list[g]-1:
                        # Once grid converted to 2D array, perform searches
                        greedy_search(grid, m_list[g], n_list[g], s_row, s_col, g_row, g_col, g, output_file)
                        a_search(grid, m_list[g], n_list[g], s_row, s_col, g_row, g_col, output_file)
                        line = file.readline()
                    else:
                        break
                else:
                    if ch == "S":
                        # Stores Starting position of grid
                        s_row = row
                        s_col = col
                    elif ch == "G":
                        # Stores Goal position of the grid
                        g_row = row
                        g_col = col
                    grid[row][col] = ch
                    col = col + 1
    file.close()
    return


def greedy_search(grid, m, n, s_row, s_col, g_row, g_col, grid_number, output_file):
    # Performs greedy search algorithm on a single grid
    frontier_rows = []
    frontier_cols = []
    frontier_priorities = []
    frontier = [frontier_rows, frontier_cols, frontier_priorities]
    start_node = [s_row, s_col, 0, "R" + str(s_row + 1) + "C" + str(s_col + 1)]
    goal_node = [g_row, g_col, 0, "R" + str(g_row + 1) + "C" + str(g_col + 1)]

    # Follows format outlined in assignment instructions
    frontier = put(frontier, start_node)
    came_from = {start_node[3]: None}

    while len(frontier[2]) != 0:
        current_node = get(frontier)
        if current_node[3] == goal_node[3]:
            break

        neighbours = get_neighbours(grid, current_node, output_file)
        for i in range(len(neighbours)):
            if neighbours[i][3] not in came_from:
                if output_file == "pathfinding_a_out.txt":
                    # Use manhattan heuristic for a_out file (only moves up/down/left/right)
                    h = "manhattan"
                else:
                    # Use chebyshev heuristic for b_out file (includes diagonal moves)
                    h = "chebyshev"
                neighbours[i][2] = heuristic(goal_node, neighbours[i], h)
                frontier = put(frontier, neighbours[i])
                came_from.update({neighbours[i][3] : current_node[3]})

    # Backtracks through the came_from dictionary to insert Ps along the path visited from S to G
    revert_rows = []
    revert_cols = []
    current_node = goal_node
    while True:
        current_node[3] = came_from.get(current_node[3])
        if current_node[3] == start_node[3]:
            break
        row = int(current_node[3][current_node[3].find("R")+1:current_node[3].find("C")]) - 1
        col = int(current_node[3][current_node[3].find("C")+1:]) - 1
        grid[row][col] = "P"
        revert_rows.append(row)
        revert_cols.append(col)

    # Writes the completed grid to the output file
    if grid_number == 0:
        file = open(output_file, "w+")
    else:
        file = open(output_file, "a+")
    file.write("Greedy\n")
    for row in range(m):
        for col in range(n):
            file.write(grid[row][col])
            if col == n - 1:
                file.write("\n")
    file.close()

    # Changes the grid back to its original (removes the Ps) so A* search algorithm can use the original grid
    for i in range(len(revert_rows)):
        grid[revert_rows[i]][revert_cols[i]] = "_"

    return


def heuristic(goal_node, neighbour, h):
    # Returns the "heuristic" cost of moving from the neighbour node to the goal node
    goal_row = goal_node[0]
    goal_col = goal_node[1]
    neighbour_row = neighbour[0]
    neighbour_col = neighbour[1]
    if h == "manhattan":
        result = abs(goal_row - neighbour_row) + abs(goal_col - neighbour_col)
    else:
        result = max(abs(neighbour_row - goal_row), abs(neighbour_col - goal_col))
    return result


def get_neighbours(grid, node, output_file):
    # Retrieves each possible neighbour
    # Checks if neighbouring position is empty or the Goal position, then appends when true
    neighbours = []
    if grid[node[0]+1][node[1]] == "_" or grid[node[0]+1][node[1]] == "G":                      # down
        neighbours.append([node[0]+1, node[1], 0, "R" + str(node[0]+2) + "C" + str(node[1]+1)])
    if grid[node[0]-1][node[1]] == "_" or grid[node[0]-1][node[1]] == "G":                      # up
        neighbours.append([node[0]-1, node[1], 0, "R" + str(node[0]) + "C" + str(node[1]+1)])
    if grid[node[0]][node[1]+1] == "_" or grid[node[0]][node[1]+1] == "G":                      # right
        neighbours.append([node[0], node[1]+1, 0, "R" + str(node[0]+1) + "C" + str(node[1]+2)])
    if grid[node[0]][node[1]-1] == "_" or grid[node[0]][node[1]-1] == "G":                      # left
        neighbours.append([node[0], node[1]-1, 0, "R" + str(node[0]+1) + "C" + str(node[1])])
    if output_file == "pathfinding_b_out.txt":
        if grid[node[0]+1][node[1]+1] == "_" or grid[node[0]+1][node[1]+1] == "G":              # down-and-right
            neighbours.append([node[0]+1, node[1]+1, 0, "R" + str(node[0]+2) + "C" + str(node[1]+2)])
        if grid[node[0]+1][node[1]-1] == "_" or grid[node[0]+1][node[1]-1] == "G":              # down-and-left
            neighbours.append([node[0]+1, node[1]-1, 0, "R" + str(node[0]+2) + "C" + str(node[1])])
        if grid[node[0]-1][node[1]+1] == "_" or grid[node[0]-1][node[1]+1] == "G":              # up-and-right
            neighbours.append([node[0]-1, node[1]+1, 0, "R" + str(node[0]) + "C" + str(node[1]+2)])
        if grid[node[0]-1][node[1]-1] == "_" or grid[node[0]-1][node[1]-1] == "G":              # up-and-left
            neighbours.append([node[0]-1, node[1]-1, 0, "R" + str(node[0]) + "C" + str(node[1])])
    return neighbours


def put(frontier, node):
    # Places node in the frontier
    # Keep frontier ordered by priority (lower is better)
    if len(frontier[2]) == 0:
        for i in range(3):
            frontier[i].append(node[i])
    else:
        index = len(frontier[2])
        for i in range(len(frontier[2])):
            if node[2] < frontier[2][i]:
                index = i
                break
        for f in range(3):
            frontier[f].insert(index, node[f])
    return frontier


def get(frontier):
    # Returns and removes the node at the start of the frontier (lowest priority value)
    current_node = []
    for i in range(3):
        current_node.append(frontier[i][0])
        frontier[i].pop(0)
    current_node.append("R" + str(current_node[0] + 1) + "C" + str(current_node[1] + 1))
    return current_node


def a_search(grid, m, n, s_row, s_col, g_row, g_col, output_file):
    # Adopts function structure of greedy search
    # Modified to follow format of A* search algorithm included in assignment instructions
    frontier_rows = []
    frontier_cols = []
    frontier_priorities = []
    frontier = [frontier_rows, frontier_cols, frontier_priorities]
    start_node = [s_row, s_col, 0, "R" + str(s_row + 1) + "C" + str(s_col + 1)]
    goal_node = [g_row, g_col, 0, "R" + str(g_row + 1) + "C" + str(g_col + 1)]
    frontier = put(frontier, start_node)
    came_from = {start_node[3]: None}
    # Includes the cost to get to current node
    # Main difference between greedy search and A* search
    cost_so_far = {start_node[3]: 0}

    while len(frontier[2]) != 0:
        current_node = get(frontier)
        if current_node[3] == goal_node[3]:
            break

        neighbours = get_neighbours(grid, current_node, output_file)
        for i in range(len(neighbours)):
            new_cost = cost_so_far.get(current_node[3]) + cost(current_node, neighbours[i])
            if neighbours[i][3] not in came_from or new_cost < cost_so_far.get(neighbours[i][3]):
                cost_so_far.update({neighbours[i][3]: new_cost})
                if output_file == "pathfinding_a_out.txt":
                    h = "manhattan"
                else:
                    h = "chebyshev"
                neighbours[i][2] = new_cost + heuristic(goal_node, neighbours[i], h)
                frontier = put(frontier, neighbours[i])
                came_from.update({neighbours[i][3]: current_node[3]})

    current_node = goal_node
    while True:
        current_node[3] = came_from.get(current_node[3])
        if current_node[3] == start_node[3]:
            break
        row = int(current_node[3][current_node[3].find("R") + 1:current_node[3].find("C")]) - 1
        col = int(current_node[3][current_node[3].find("C") + 1:]) - 1
        grid[row][col] = "P"

    file = open(output_file, "a+")
    file.write("A*\n")
    for row in range(m):
        for col in range(n):
            file.write(grid[row][col])
            if col == n - 1:
                file.write("\n")
    file.write("\n")
    file.close()
    return


def cost(current_node, neighbour):
    # Cost per search move
    return 1


def main():
    path_creator.write_files()
    m_list = find_m_values("pathfinding_a.txt")
    n_list = find_n_values("pathfinding_a.txt")
    convert_and_searches("pathfinding_a.txt", m_list, n_list, "pathfinding_a_out.txt")

    m_list = find_m_values("pathfinding_b.txt")
    n_list = find_n_values("pathfinding_b.txt")
    convert_and_searches("pathfinding_b.txt", m_list, n_list, "pathfinding_b_out.txt")


main()
