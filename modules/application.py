import pygame
from itertools import cycle
from modules.grid import Grid
from modules.cell import CellType
from modules.pathfinder import Pathfinder
from settings import *


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

        self.pathfinder = Pathfinder(self.grid)
        self.pathfinder_algorithm_cycle = cycle(self.pathfinder.algorithms)
        self.pathfinder.current_algorithm = next(self.pathfinder_algorithm_cycle)
        pygame.display.set_caption(f'Pathfinding: {self.pathfinder.current_algorithm}')

    def select_point(self, cell_index, point_type):
        if point_type == CellType.START:
            start_cell = self.grid.get_start_cell()
            if start_cell != cell_index:
                if start_cell is not None:
                    self.grid.cells[start_cell].cell_type = CellType.EMPTY
                self.grid.cells[cell_index].cell_type = CellType.START

        if point_type == CellType.END:
            end_cell = self.grid.get_end_cell()
            if end_cell != cell_index:
                if end_cell is not None:
                    self.grid.cells[end_cell].cell_type = CellType.EMPTY
                self.grid.cells[cell_index].cell_type = CellType.END

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
            self.pathfinder.current_algorithm = next(self.pathfinder_algorithm_cycle)
            pygame.display.set_caption(f'Pathfinding: {self.pathfinder.current_algorithm}')
            self.actions['SELECT_PATHFINDER'] = False

        if self.actions['START_PATHFINDING']:
            start_cell = self.grid.get_start_cell()
            end_cell = self.grid.get_end_cell()

            if start_cell is not None and end_cell is not None:
                if start_cell == end_cell:
                    self.actions['START_PATHFINDING'] = False
                else:
                    self.pathfinder.update_path()

    def draw(self):
        self.grid.draw(self.main_surface)

        if self.actions['START_PATHFINDING']:
            self.pathfinder.draw_path(self.main_surface)
            self.actions['START_PATHFINDING'] = False

        self.window.blit(self.main_surface, (0, 0))

        pygame.display.update()

    def run(self):
        while self.running:

            self.update()
            self.draw()

        pygame.quit()
