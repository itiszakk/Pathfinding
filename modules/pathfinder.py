from modules.cell import CellType


class PathfinderAlgorithms:
    BFS = 'Breadth-First Search'
    ASTAR = 'A-Star'
    DIJKSTRA = 'Dijkstra\'s algorithm'


class Pathfinder:
    def __init__(self, grid):
        self.grid = grid
        self.algorithms = [PathfinderAlgorithms.BFS, PathfinderAlgorithms.ASTAR, PathfinderAlgorithms.DIJKSTRA]
        self.current_algorithm = PathfinderAlgorithms.BFS
        self.path = None

    def bfs(self): pass

    def a_star(self): pass

    def dijkstra(self): pass

    def update_path(self):
        if self.current_algorithm == PathfinderAlgorithms.BFS:
            self.bfs()

        if self.current_algorithm == PathfinderAlgorithms.ASTAR:
            pass

        if self.current_algorithm == PathfinderAlgorithms.DIJKSTRA:
            pass

    def draw_path(self, surface): pass

