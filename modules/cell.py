import pygame


class Cell:
    def __init__(self, position, size, outline, fill_color, outline_color):
        self.outline_surface = pygame.surface.Surface((size + 2*outline, size + 2*outline))
        self.fill_surface = pygame.surface.Surface((size, size))

        self.outline_surface.fill(outline_color)
        self.fill_surface.fill(fill_color)

        self.outline_rect = pygame.rect.Rect(position, self.outline_surface.get_size())
        self.fill_rect = pygame.rect.Rect((position[0] + outline, position[1] + outline), self.fill_surface.get_size())

    def update(self, mouse_position): pass

    def draw(self, surface):
        surface.blit(self.outline_surface, self.outline_rect.topleft)
        surface.blit(self.fill_surface, self.fill_rect.topleft)
