# Path-Finding
Uses greedy and A* search algorithms to find a path to a goal.
 
  1. Download pathfinding.py and path_creator.py
  2. Run pathfinding.py and complete the prompts in the console.
  3. Output files will be generated in local folder (examples of these in ExampleFiles folder in repo).
     a) pathfinding_a.txt and pathfinding_b.txt are grids that have been randomly generated by path_creator.py
        Each starting grid has a starting position and a goal position. 
        Additionally, the grid has a boundary and randomly generated obstacles located within the grid.
     b) pathfinding_a_out.txt and pathfinding_b_out.txt are the solved versions of these maps/grids.
        pathfinding.py uses both greedy and A* search algorithms to find solutions.

How to Interpret Output Files:
 X = border surrounding map + randomly generated obstacles within grid
 _ = empty spaces on grid
 S = starting position
 G = goal position
 P = path travelled to reach goal from start
