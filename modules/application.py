import pygame

from modules.json_handler import read_json, write_json
from modules.grid import Grid


class PathfindingApplication:
    def __init__(self):
        pygame.init()

        self.running = True

        self.settings = read_json('data\\settings.json')

        self.window = pygame.display.set_mode((self.settings['window']['width'], self.settings['window']['height']))
        self.main_surface = pygame.Surface(self.window.get_size())
        self.clock = pygame.time.Clock()

        self.actions = {
            'SELECT_POINT': False,
            'SELECT_BLOCK': False,
            'SELECT_PATHFINDER': False,
            'START_PATHFINDING': False,
            'RESET_GRID': False
        }

        self.grid = Grid(self.settings, self.window.get_rect().center)

    def change_settings(self):
        write_json(self.settings, 'data\\settings.json')

    def poll_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.mouse_events(event)
            self.keyboard_events(event)

    def mouse_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:

            left_button, right_button, middle_button = pygame.mouse.get_pressed()

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
        mouse_position = pygame.mouse.get_pos()

        self.main_surface.fill(self.settings['color']['background'])

        self.poll_events()
        self.grid.update(mouse_position)


    def draw(self):
        self.grid.draw(self.main_surface)

        self.window.blit(pygame.transform.scale(self.main_surface, self.window.get_size()), (0, 0))

        pygame.display.update()

    def run(self):
        while self.running:
            self.clock.tick(self.settings['window']['framerate'])

            self.update()
            self.draw()

        pygame.quit()
