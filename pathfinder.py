import argparse
import numpy as np
from collections import deque
import heapq

class Problem:
    def __init__(self, initial_state, goal_state, map_grid):
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.map_grid = map_grid
    
    def goal_test(self, state):
        return state == self.goal_state

class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

def expand(node, problem):
    children = []
    i, j = node.state
    adjacent_positions = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]  # Up, Down, Left, Right
    
    for position in adjacent_positions:
        if is_valid_position(position, problem.map_grid):
            elevation = int(problem.map_grid[position[0] - 1][position[1] - 1])
            child_node = make_node(position, node, path_cost=node.path_cost + elevation)
            children.append(child_node)
    
    return children


def make_node(state, parent=None, action=None, path_cost=0):
    return Node(state, parent, action, path_cost)

def is_valid_position(position, grid):
    i, j = position
    return 0 < i <= len(grid) and 0 < j <= len(grid[0]) and grid[i - 1][j - 1] != 'X'

# Function to parse the map input from a file
def parse_map(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        rows, cols = map(int, lines[0].split())
        start_position = tuple(map(int, lines[1].split()))
        end_position = tuple(map(int, lines[2].split()))
        map_grid = [list(map(str.strip, lines[i].split())) for i in range(3, rows + 3)]
        return rows, cols, start_position, end_position, map_grid

# Function to perform Breadth First Search (BFS)
def bfs_search(problem):
    closed = set()
    fringe = deque([make_node(problem.initial_state)])
    
    while fringe:
        node = fringe.popleft()
        
        if problem.goal_test(node.state):
            return node
        
        if node.state not in closed:
            closed.add(node.state)
            fringe.extend(expand(node, problem))
    
    return None

# Function to print the map
def print_map(map_grid):
    for row in map_grid:
        print(" ".join(row))

# Function to print the solution
def print_solution(map_grid, path):
    for i, row in enumerate(map_grid):
        row_list = list(row)
        for j, _ in enumerate(row_list):
            if (i + 1, j + 1) in path:
                row_list[j] = '*'
        print(' '.join(row_list))

def reconstruct_path(solution):
    path = []
    current = solution
    while current is not None:
        path.append(current.state)
        current = current.parent
    return path[::-1]


def arg_parser():
    parser = argparse.ArgumentParser(description='Pathfinder')
    parser.add_argument('map', type=str, help='text file of map')
    parser.add_argument('algorithm', type=str, help='choose algorithm', choices=['bfs', 'a-star', 'ucs'])
    parser.add_argument('heuristic', type=str, help='heuristic function', choices=['manhattan', 'euclidean'])
    return parser.parse_args()

def main():
    args = arg_parser()
    map_file = args.map
    rows, cols, start_position, end_position, map_grid = parse_map(map_file)
    problem = Problem(start_position, end_position, map_grid)

    solution = bfs_search(problem)

    if solution:
        print('MAP:')
        print_map(map_grid)
        print("BFS Solution found:", solution.state)
        print_solution(map_grid, reconstruct_path(solution))
    else:
        print("BFS: No solution found.")
    
if __name__ == "__main__":
    main()