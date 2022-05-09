from collections import deque
import heapq

from modules.grid import Grid
from modules.cell import CellType


class PathfinderAlgorithms:
    BFS = 'Breadth-First Search'
    ASTAR = 'A-Star'
    DIJKSTRA = 'Dijkstra\'s algorithm'

# TODO PathfinderManager
# TODO Algorithm in file


class Pathfinder:
    def __init__(self, grid: Grid):
        self.running = False
        self.calculating = False
        self.grid = grid
        self.start_cell = None
        self.end_cell = None
        self.current_algorithm = PathfinderAlgorithms.BFS
        self.algorithms = [PathfinderAlgorithms.BFS, PathfinderAlgorithms.ASTAR, PathfinderAlgorithms.DIJKSTRA]
        self.path = []
        self.visited = {}
        self.queue = deque()

    def clear(self):
        self.queue.clear()
        self.visited.clear()
        self.path.clear()
        self.grid.clear_path()
        self.start_cell = None
        self.end_cell = None

    def start(self):
        self.clear()

        if self.current_algorithm == PathfinderAlgorithms.BFS:
            self.start_cell = self.grid.get_start_cell()
            self.end_cell = self.grid.get_end_cell()
            self.queue.append(self.start_cell)
            self.visited[self.start_cell] = None
        elif self.current_algorithm == PathfinderAlgorithms.ASTAR: pass
        elif self.current_algorithm == PathfinderAlgorithms.DIJKSTRA: pass

        self.running = True
        self.calculating = True

    def stop(self):
        self.clear()
        self.running = False

    def update(self):
        if self.running and self.calculating:
            if self.current_algorithm == PathfinderAlgorithms.BFS:

                if self.queue:
                    cell = self.queue.popleft()

                    # Show visited cells each frame
                    if cell != self.start_cell and cell != self.end_cell:
                        self.grid.cells[cell].cell_type = CellType.VISITED

                    if cell == self.end_cell:
                        self.calculating = False

                    for neighbour in self.grid.get_cell_neighbours(cell):
                        if neighbour not in self.visited:
                            self.queue.append(neighbour)
                            self.visited[neighbour] = cell

            if self.current_algorithm == PathfinderAlgorithms.ASTAR:
                pass

            if self.current_algorithm == PathfinderAlgorithms.DIJKSTRA:
                pass

        if self.running and not self.calculating:
            # Find the shortest path
            path_cell = self.end_cell
            while path_cell and path_cell in self.visited:
                if path_cell is not None and path_cell != self.start_cell and path_cell != self.end_cell:
                    self.path.append(path_cell)
                path_cell = self.visited[path_cell]

            # Show path
            for path_cell in self.path:
                self.grid.cells[path_cell].cell_type = CellType.PATH

            self.running = False

