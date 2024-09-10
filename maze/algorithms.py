from .datastructures import Cell, Node, StackFrontier, Grid, QueueFrontier


class DepthFirstSearch:
    Frontier = StackFrontier
    def __init__(self, maze: Grid, start: Cell, end: Cell):
        self.frontier = self.Frontier()
        self.explored = set()
        self.start = Node(start, None, None)
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
                child = Node(neighbour, parent=node, action=None)
                if child.state.cell_type != 'wall':
                    self.frontier.add(child)

        if node.state.cell_type not in ['start', 'end']: node.state.set_cell_type('exp')

        return node

    def backpropagate(self) -> list[Node]:
        return self.solution
        

class BreadthFirstSearch(DepthFirstSearch):
    Frontier = QueueFrontier

algoritms_mapping = {
    'dfs': DepthFirstSearch,
    'bfs': BreadthFirstSearch 
}