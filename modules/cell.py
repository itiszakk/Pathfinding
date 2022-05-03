import pygame
from enum import IntEnum
from settings import *


class CellType(IntEnum):
    EMPTY = 0
    BLOCKED = 1
    START = 2
    END = 3
    PATH = 4


class Cell:
    def __init__(self, position):
        self.outline_surface = pygame.surface.Surface((CELL_SIZE + 2 * CELL_OUTLINE, CELL_SIZE + 2 * CELL_OUTLINE))
        self.fill_surface = pygame.surface.Surface((CELL_SIZE, CELL_SIZE))

        self.outline_rect = pygame.rect.Rect(position, self.outline_surface.get_size())
        self.fill_rect = pygame.rect.Rect(
            (position[0] + CELL_OUTLINE, position[1] + CELL_OUTLINE),
            self.fill_surface.get_size()
        )

        self.cell_type = CellType.EMPTY
        self.set_outline_color(OUTLINE_COLOR)

    def set_outline_color(self, color):
        self.outline_surface.fill(color)

    def set_fill_color(self, color):
        self.fill_surface.fill(color)

    def clicked(self, mouse_position):
        return self.outline_rect.collidepoint(mouse_position)

    def update(self):
        if self.cell_type == CellType.EMPTY:
            self.set_fill_color(EMPTY_CELL_COLOR)
        if self.cell_type == CellType.BLOCKED:
            self.set_fill_color(BLOCKED_CELL_COLOR)
        if self.cell_type == CellType.START:
            self.set_fill_color(START_CELL_COLOR)
        if self.cell_type == CellType.END:
            self.set_fill_color(END_CELL_COLOR)
        if self.cell_type == CellType.PATH:
            self.set_fill_color(PATH_CELL_COLOR)

    def draw(self, surface):
        surface.blit(self.outline_surface, self.outline_rect.topleft)
        surface.blit(self.fill_surface, self.fill_rect.topleft)
