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

    def get_start_cell(self):
        for index, cell in enumerate(self.cells):
            if cell.cell_type == CellType.START:
                return index
        return None

    def get_end_cell(self):
        for index, cell in enumerate(self.cells):
            if cell.cell_type == CellType.END:
                return index
        return None

    def get_clicked_cell(self, mouse_position):
        for index, cell in enumerate(self.cells):
            if cell.clicked(mouse_position):
                return index
        return None

    def get_cell_neighbours(self, cell_index):
        neighbours = []

        row = int(cell_index / GRID_COLUMNS)
        column = cell_index - row * GRID_COLUMNS

        get_index = lambda x, y: x * GRID_COLUMNS + y

        if row > 0:
            if self.cells[get_index(row - 1, column)].cell_type != CellType.BLOCKED:
                neighbours.append(get_index(row - 1, column))

        if column > 0:
            if self.cells[get_index(row, column - 1)].cell_type != CellType.BLOCKED:
                neighbours.append(get_index(row, column - 1))

        if row < GRID_ROWS - 1:
            if self.cells[get_index(row + 1, column)].cell_type != CellType.BLOCKED:
                neighbours.append(get_index(row + 1, column))

        if column < GRID_COLUMNS - 1:
            if self.cells[get_index(row, column + 1)].cell_type != CellType.BLOCKED:
                neighbours.append(get_index(row, column + 1))

        return neighbours

    def update(self):
        for cell in self.cells:
            cell.update()

    def draw(self, surface):
        for cell in self.cells:
            cell.draw(self.grid_surface)

        surface.blit(self.grid_surface, self.grid_surface.get_rect())

    def reset(self):
        for cell in self.cells:
            cell.cell_type = CellType.EMPTY
