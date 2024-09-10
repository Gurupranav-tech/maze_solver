from .constants import *
import pygame


class Cell:
    def __init__(self, cell_type: str, w: int, h: int):
        self.cell_type = cell_type
        self.width = w
        self.height = h
        self.rect = (self.width * SCALE, self.height * SCALE, SCALE,SCALE)

        if cell_type == 'wall':
            self.color = BLACK
        elif cell_type == 'start':
            self.color = GREEN
        elif cell_type == 'end':
            self.color = RED
        elif cell_type == 'exp':
            self.color = BLUE
        elif cell_type == 'fin':
            self.color = YELLOW
        else:
            self.color = WHITE

    def render(self, surface: pygame.Surface):
        pygame.draw.rect(surface, self.color, self.rect)
    
    def set_cell_type(self, cell_type: str):
        self.cell_type =cell_type
        if cell_type == 'wall':
            self.color = BLACK
        elif cell_type == 'start':
            self.color = GREEN
        elif cell_type == 'end':
            self.color = RED
        elif cell_type == 'exp':
            self.color = BLUE
        elif cell_type == 'fin':
            self.color = YELLOW
        else:
            self.color = WHITE

    def __repr__(self) -> str:
        return f'Cell(color={self.color}, type={self.cell_type}, x={self.width}, y={self.height})'
    

class Grid(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start: Cell = None
        self.end: Cell = None

    def set_start(self, start: Cell):
        self.start = start

    def set_end(self, end: Cell):
        self.end = end

    def get_neighbours(self, node: Cell):
        w, h = node.width, node.height
        neighbours: list[Cell] = []

        if w > 0:
            neighbours.append(self[h][w-1])
        if h > 0:
            neighbours.append(self[h-1][w])
        if w < len(self[0])-1:
            neighbours.append(self[h][w+1])
        if h < len(self)-1:
            neighbours.append(self[h+1][w])

        return neighbours


class Node:
    def __init__(self, state: Cell, parent):
        self.state: Cell = state
        self.parent: Node = parent

    def __str__(self) -> str:
        return f'{self.state}'


class StackFrontier:
    def __init__(self):
        self.frontier: list[Node] = []

    def add(self, node: Node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)
    
    def empty(self):
        return len(self.frontier) == 0
    
    def remove(self) -> Node :
        if self.empty():
            return None

        return self.frontier.pop()


class QueueFrontier(StackFrontier):
    def remove(self) -> Node:
        if self.empty():
            return None
        node = self.frontier[0]
        self.frontier = self.frontier[1:]
        return node