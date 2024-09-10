import pygame
import sys
from maze import *
from maze.utils import parse_args, read_maze, render_grid, solve
from maze.algorithms import algoritms_mapping


def main():
    maze_file, alg, mode = parse_args()
    if alg not in algoritms_mapping.keys():
        print('Unknown Algorithm. Only BFS, DFS are available.')
        sys.exit(1)

    width, height, maze = read_maze(maze_file)

    WIDTH=width * SCALE
    HEIGHT=height * SCALE

    pygame.init()
    window: pygame.Surface = pygame.display.set_mode((WIDTH, HEIGHT))
    done = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if done: continue
                stat = solve(alg, mode, maze, window)
                if not stat:
                    print('No soln')
                    sys.exit(1)
                else:
                    done = True 

        window.fill(WHITE)

        render_grid(window, maze)

        pygame.display.update()


if __name__ == '__main__':
    main()