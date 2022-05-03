import pygame
from enum import IntEnum
from itertools import cycle
from modules.grid import Grid
from modules.cell import CellType
from settings import *


class PathfinderAlgorithms(IntEnum):
    BFS = 0
    A_STAR = 1
    DIJKSTRA = 2


class PathfindingApplication:
    def __init__(self):
        pygame.init()

        self.running = True

        self.window = pygame.display.set_mode((
            GRID_COLUMNS * (CELL_SIZE + CELL_OUTLINE) + CELL_OUTLINE,
            GRID_ROWS * (CELL_SIZE + CELL_OUTLINE) + CELL_OUTLINE
        ))

        self.main_surface = pygame.Surface(self.window.get_size())

        self.actions = {
            'SELECT_POINT': False,
            'SELECT_BLOCK': False,
            'SELECT_PATHFINDER': False,
            'START_PATHFINDING': False,
            'RESET_GRID': False
        }

        self.grid = Grid()

        self.point_type_cycle = cycle([CellType.START, CellType.END])

        self.pathfinder_names = ['Breadth-First Search', 'A-Star', 'Dijkstra\'s algorithm']
        self.current_pathfinder = PathfinderAlgorithms.BFS

        pygame.display.set_caption(f'Pathfinding: {self.pathfinder_names[self.current_pathfinder]}')

    def bfs_pathfinder(self): pass

    def a_star_pathfinder(self): pass

    def dijkstra_pathfinder(self): pass

    def select_point(self, cell_point_index, point_type):
        for index, cell in enumerate(self.grid.cells):
            if cell.cell_type == point_type and index != cell_point_index:
                cell.cell_type = CellType.EMPTY

        self.grid.cells[cell_point_index].cell_type = point_type

    def poll_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.mouse_events(event)
            self.keyboard_events(event)

    def mouse_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:

            left_button, middle_button, right_button = pygame.mouse.get_pressed()

            if left_button:
                self.actions['SELECT_POINT'] = True

            if right_button:
                self.actions['SELECT_BLOCK'] = True

        if event.type == pygame.MOUSEBUTTONUP:
            self.actions['SELECT_POINT'] = False
            self.actions['SELECT_BLOCK'] = False

    def keyboard_events(self, event):
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_p:
                self.actions['SELECT_PATHFINDER'] = True

            if event.key == pygame.K_SPACE:
                self.actions['START_PATHFINDING'] = True

            if event.key == pygame.K_r:
                self.actions['RESET_GRID'] = True

        if event.type == pygame.KEYUP:
            self.actions['SELECT_PATHFINDER'] = False
            self.actions['START_PATHFINDING'] = False
            self.actions['RESET_GRID'] = False

    def update(self):
        self.main_surface.fill(BACKGROUND_COLOR)

        self.poll_events()
        self.grid.update()

        if self.actions['SELECT_POINT']:
            mouse_position = pygame.mouse.get_pos()
            clicked_cell = self.grid.get_clicked_cell(mouse_position)
            if clicked_cell is not None:
                point_type = next(self.point_type_cycle)
                self.select_point(clicked_cell, point_type)
            self.actions['SELECT_POINT'] = False

        if self.actions['SELECT_BLOCK']:
            mouse_position = pygame.mouse.get_pos()
            clicked_cell = self.grid.get_clicked_cell(mouse_position)
            if clicked_cell is not None:
                self.grid.cells[clicked_cell].cell_type = CellType.BLOCKED

        if self.actions['RESET_GRID']:
            self.grid.reset()
            self.actions['RESET_GRID'] = False

        if self.actions['SELECT_PATHFINDER']:
            if self.current_pathfinder == PathfinderAlgorithms.BFS:
                self.current_pathfinder = PathfinderAlgorithms.A_STAR
            elif self.current_pathfinder == PathfinderAlgorithms.A_STAR:
                self.current_pathfinder = PathfinderAlgorithms.DIJKSTRA
            elif self.current_pathfinder == PathfinderAlgorithms.DIJKSTRA:
                self.current_pathfinder = PathfinderAlgorithms.BFS

            pygame.display.set_caption(f'Pathfinding: {self.pathfinder_names[self.current_pathfinder]}')
            self.actions['SELECT_PATHFINDER'] = False

        if self.actions['START_PATHFINDING']:
            if self.current_pathfinder == PathfinderAlgorithms.BFS:
                self.bfs_pathfinder()
            if self.current_pathfinder == PathfinderAlgorithms.A_STAR:
                self.a_star_pathfinder()
            if self.current_pathfinder == PathfinderAlgorithms.DIJKSTRA:
                self.dijkstra_pathfinder()

            self.actions['START_PATHFINDING'] = False

    def draw(self):
        self.grid.draw(self.main_surface)
        self.window.blit(self.main_surface, (0, 0))
        pygame.display.update()

    def run(self):
        while self.running:

            self.update()
            self.draw()

        pygame.quit()
