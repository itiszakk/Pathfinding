import pygame
from modules.cell import Cell


class Grid:
    def __init__(self, settings, position):
        self.settings = settings
        self.position = position

        self.cells = []
        for i in range(self.settings['grid']['rows']):
            for j in range(self.settings['grid']['columns']):
                cell_size = self.settings['grid']['cell_size']
                cell_outline = self.settings['grid']['outline']

                cell_offset = cell_size + cell_outline
                cell_position = (j * cell_offset, i * cell_offset)

                cell_fill_color = self.settings['color']['empty_cell']
                cell_outline_color = self.settings['color']['outline']

                self.cells.append(Cell(cell_position, cell_size, cell_outline, cell_fill_color, cell_outline_color))

        self.grid_surface = pygame.surface.Surface(self.cells[-1].outline_rect.bottomright)

    def update(self, mouse_position): pass

    def draw(self, surface):
        for cell in self.cells:
            cell.draw(self.grid_surface)

        surface.blit(self.grid_surface, self.grid_surface.get_rect(center=self.position))
