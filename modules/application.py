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

        self.clock = pygame.time.Clock()

        self.main_surface = pygame.Surface(self.window.get_size())

        self.actions = {
            'SELECT_POINT': False,
            'SELECT_BLOCK': False,
            'SELECT_PATHFINDER': False,
            'RESET_GRID': False,
            'RESTART_PATHFINDER': False
        }

        self.grid = Grid()
        self.select_point_cycle = cycle([self.select_start_cell, self.select_end_cell])

        self.pathfinder = Pathfinder(self.grid)
        self.pathfinder_algorithm_cycle = cycle(self.pathfinder.algorithms)
        self.pathfinder.current_algorithm = next(self.pathfinder_algorithm_cycle)
        pygame.display.set_caption(f'Pathfinding: {self.pathfinder.current_algorithm}')

    def select_start_cell(self, cell_index):
        start_cell = self.grid.get_start_cell()
        if start_cell != cell_index:
            if start_cell is not None:
                self.grid.cells[start_cell].cell_type = CellType.EMPTY
            self.grid.cells[cell_index].cell_type = CellType.START

    def select_end_cell(self, cell_index):
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

            if event.key == pygame.K_r:
                self.actions['RESET_GRID'] = True

        if event.type == pygame.KEYUP:
            self.actions['SELECT_PATHFINDER'] = False
            self.actions['RESET_GRID'] = False

    def actions_handler(self):
        if self.actions['SELECT_POINT']:
            mouse_position = pygame.mouse.get_pos()
            clicked_cell = self.grid.get_clicked_cell(mouse_position)

            if clicked_cell is not None:
                select_point_func = next(self.select_point_cycle)
                select_point_func(clicked_cell)

                start_cell = self.grid.get_start_cell()
                end_cell = self.grid.get_end_cell()

                if start_cell is not None and end_cell is not None and start_cell != end_cell:
                    self.pathfinder.start()
                else:
                    self.pathfinder.stop()

            self.actions['SELECT_POINT'] = False

        if self.actions['SELECT_BLOCK']:
            mouse_position = pygame.mouse.get_pos()
            clicked_cell = self.grid.get_clicked_cell(mouse_position)
            start_cell = self.grid.get_start_cell()
            end_cell = self.grid.get_end_cell()
            if clicked_cell is not None and clicked_cell != start_cell and clicked_cell != end_cell:
                self.grid.cells[clicked_cell].cell_type = CellType.BLOCKED

            if start_cell is not None and end_cell is not None and start_cell != end_cell:
                self.pathfinder.stop()
                self.actions['RESTART_PATHFINDER'] = True

        if not self.actions['SELECT_BLOCK'] and self.actions['RESTART_PATHFINDER']:
            self.pathfinder.start()
            self.actions['RESTART_PATHFINDER'] = False

        if self.actions['RESET_GRID']:
            self.grid.reset()
            self.pathfinder.stop()
            self.actions['RESET_GRID'] = False

        if self.actions['SELECT_PATHFINDER']:
            self.pathfinder.current_algorithm = next(self.pathfinder_algorithm_cycle)
            pygame.display.set_caption(f'Pathfinding: {self.pathfinder.current_algorithm}')
            self.pathfinder.stop()
            self.grid.reset()
            self.actions['SELECT_PATHFINDER'] = False

    def update(self):
        self.main_surface.fill(BACKGROUND_COLOR)

        self.poll_events()

        self.grid.update()

        self.actions_handler()

        self.pathfinder.update()

    def draw(self):
        self.grid.draw(self.main_surface)
        self.window.blit(self.main_surface, (0, 0))

        pygame.display.update()

    def run(self):
        while self.running:
            self.update()
            self.draw()

        pygame.quit()
