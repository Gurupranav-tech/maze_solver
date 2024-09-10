import sys
from .datastructures import Grid, Cell
from .algorithms import *
from .constants import *
import pygame


def solve(alg: str, mode: str, maze: Grid, window: pygame.Surface):
    Solver = algoritms_mapping[alg]
    solver = Solver(maze, maze.start, maze.end)
    first = True 

    if mode == 'normal':
        while True:
            status = solver.next() 
            if status is None:
                return False

            if status.state == maze.end:
                parents = solver.backpropagate()
                for parent in parents:
                    if parent.state not in [maze.start, maze.end]: parent.state.set_cell_type('fin')
                return True
            
    elif mode == 'manual':
        over = False
        ctn = True
        while not over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                if event.type == pygame.KEYDOWN:
                    ctn = True

            if not ctn:
                continue

            status = solver.next()
            if status is None:
                return False

            if status.state == maze.end:
                parents = solver.backpropagate()
                for parent in parents:
                    if parent.state not in [maze.start, maze.end]: parent.state.set_cell_type('fin')
                return True


            render_grid(window, maze)


            if first:
                first = False
                continue
            ctn = False


def render_grid(window: pygame.Surface, grid: list[list[Cell]]):
    window.fill(BLACK)
    for line in (grid):
        for chr in (line):
            chr.render(window)
    pygame.display.update()


def parse_args():
    if len(sys.argv) < 3:
        print('usage error: python maze.py [mazefile] [algorithm] [optional:mode] [optional:grid_size]')
        sys.exit(1)

    maze_file = sys.argv[1]
    alg = sys.argv[2]

    if len(sys.argv) >= 4:
        mode = sys.argv[3]
        return (maze_file, alg, mode)

    return (maze_file, alg, 'normal')


def read_maze(file: str) -> tuple[int, int, Grid]:
    maze = Grid()
    with open(file) as f:
        content = f.read()

    lines = content.splitlines()
    height = len(lines)
    width = max(len(l) for l in lines)

    for w, line in enumerate(lines):
        m  = []
        for h, chr in enumerate(line):
            if chr == ' ': m.append(Cell('path', h, w))
            elif chr == '#': m.append(Cell('wall', h, w))
            elif chr == 'A': 
                cell = Cell('start', h, w)
                m.append(cell)
                maze.set_start(cell)
            elif chr == 'B':
                cell = Cell('end', h, w)
                m.append(cell)
                maze.set_end(cell)
        maze.append(m)


    return (width, height, maze)
