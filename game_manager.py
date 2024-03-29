import pygame

from objects.graph_axis import GraphAxis
from ui.hud import HUD
from objects.ground import Ground
from objects.pigeon import Pigeon
from objects.rifle import Rifle
from screen import PyGameScalableGraphScreen
from steps.boot_step import BootStep


class GameManager:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.clock = pygame.time.Clock()
        self.done = False

        sky = pygame.Color(120, 173, 226)
        pigeon = pygame.Color(0, 45, 91)
        riffle = pygame.Color(142, 40, 0)
        hud = pygame.Color(168, 211, 255)
        title = pygame.Color(0, 45, 91)
        text = pygame.Color(0, 22, 45)
        ground = pygame.Color(106, 67, 51)

        axis_main_color = pygame.Color(0, 0, 0, 128)
        axis_secondary_color = pygame.Color(0, 0, 0, 32)
        points_color = pygame.Color(255, 255, 255)
        points_radius = 7
        axis_width = 5

        self.screen = PyGameScalableGraphScreen("Tire au pigeon", 1600, 900, sky)

        self.pigeon = Pigeon(pigeon, axis_width, 0, 20, 1000, points_color, points_radius)
        self.rifle = Rifle(riffle, axis_width, points_color, points_radius)
        self.ground = Ground(ground)

        self.screen.add_drawable_object(self.ground)
        self.screen.add_drawable_object(self.pigeon)
        self.screen.add_drawable_object(self.rifle)

        self.screen.add_axe(GraphAxis("width", "meters", axis_main_color, axis_secondary_color, 25, False))
        self.screen.add_axe(GraphAxis("height", "meters", axis_main_color, axis_secondary_color, 25, True))

        self.step = BootStep(self.rifle, self.pigeon)

        self.hud = HUD("Tire au pigeon d'argile", title, text, hud, self.step)
        self.screen.add_ui(self.hud)

    def start(self):
        while not self.done:
            for event in pygame.event.get():  # User did something
                self.handle_event(event)
            self.screen.clear()
            self.update()
            self.screen.render()
        pygame.quit()

    def update(self):
        mouse_position = pygame.mouse.get_pos()
        self.step.update(self.screen, mouse_position, self.get_playtime())
        if self.step.is_done and (self.step.next_step() is not None):
            previous_step = self.step
            self.step = self.step.next_step()
            self.step.previous_step = previous_step
            self.hud.step = self.step

    def handle_event(self, event):
        if event.type == pygame.QUIT:  # If user clicked close
            self.done = True  # Flag that we are done so we exit this loop
            
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.step.previous_step is not None:
            mouse_position = pygame.mouse.get_pos()
            if 6 < mouse_position[0] < (48 + 12) and 6 < mouse_position[1] < (48 + 12):
                self.step = self.step.previous_step
                self.step.reset()
                self.hud.step = self.step

        self.step.handle_event(event)
        self.screen.handle_event(event)

    def get_playtime(self):
        return pygame.time.get_ticks() / 1000.0
