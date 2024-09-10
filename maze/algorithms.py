from .datastructures import Cell, Node, StackFrontier, Grid, QueueFrontier, GreedyFrontier


class DepthFirstSearch:
    Frontier = StackFrontier
    def __init__(self, maze: Grid, start: Cell, end: Cell):
        self.frontier = self.Frontier()
        self.explored = set()
        self.start = Node(start, None)
        self.goal = end.width, end.height
        self.maze = maze
        self.solution = []

        self.frontier.add(self.start)

    def next(self):
        if self.frontier.empty():
            return None

        node = self.frontier.remove()
        copy = node
        if (node.state.width, node.state.height) == self.goal:
            parents = []
            while node.parent is not None:
                parents.append(node)
                node = node.parent

            parents.reverse()
            self.solution = parents
            return copy

        self.explored.add((node.state.width, node.state.height))

        for neighbour in self.maze.get_neighbours(node.state):
            if not self.frontier.contains_state(neighbour) and (neighbour.width, neighbour.height) not in self.explored:
                child = Node(neighbour, parent=node)
                if child.state.cell_type != 'wall':
                    self.frontier.add(child)

        if node.state.cell_type not in ['start', 'end']: node.state.set_cell_type('exp')

        return node

    def backpropagate(self) -> list[Node]:
        return self.solution
        

class BreadthFirstSearch(DepthFirstSearch):
    Frontier = QueueFrontier


class GreedyBreadthFirstSearch(BreadthFirstSearch):
    Frontier = GreedyFrontier
    
    def __init__(self, maze: Grid, start: Cell, end: Cell):
        super().__init__(maze, start, end)
        self.start.cost = 0
    
    def next(self):
        if self.frontier.empty():
            return None

        node = self.frontier.remove()
        copy = node
        if (node.state.width, node.state.height) == self.goal:
            parents = []
            while node.parent is not None:
                parents.append(node)
                node = node.parent

            parents.reverse()
            self.solution = parents
            return copy

        self.explored.add((node.state.width, node.state.height))

        for neighbour in self.maze.get_neighbours(node.state):
            if not self.frontier.contains_state(neighbour) and (neighbour.width, neighbour.height) not in self.explored:
                child = Node(neighbour, parent=node)
                if child.state.cell_type != 'wall':
                    child.cost = self.heurestic((child.state.width, child.state.height), self.goal)
                    self.frontier.add(child)

        if node.state.cell_type not in ['start', 'end']: node.state.set_cell_type('exp')

        return node

    @staticmethod
    def heurestic(s: tuple[int, int], goal: tuple[int, int]):
        return abs(s[0] - goal[0]) + abs(s[1] - goal[1])

algoritms_mapping = {
    'dfs': DepthFirstSearch,
    'bfs': BreadthFirstSearch,
    'gbfs': GreedyBreadthFirstSearch
}