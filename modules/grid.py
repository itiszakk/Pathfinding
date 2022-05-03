import pygame
from modules.cell import Cell, CellType
from settings import *


class Grid:
    def __init__(self):
        self.cells = []
        for i in range(GRID_ROWS):
            for j in range(GRID_COLUMNS):
                self.cells.append(Cell((j * (CELL_SIZE + CELL_OUTLINE), i * (CELL_SIZE + CELL_OUTLINE))))

        self.grid_surface = pygame.surface.Surface(self.cells[-1].outline_rect.bottomright)

    def get_clicked_cell(self, mouse_position):
        for index, cell in enumerate(self.cells):
            if cell.clicked(mouse_position):
                return index
        return None

    def reset(self):
        for cell in self.cells:
            cell.cell_type = CellType.EMPTY

    def update(self):
        for cell in self.cells:
            cell.update()

    def draw(self, surface):
        for cell in self.cells:
            cell.draw(self.grid_surface)

        surface.blit(self.grid_surface, self.grid_surface.get_rect())