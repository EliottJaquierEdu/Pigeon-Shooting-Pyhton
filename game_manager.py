import pygame

from graph_axis import GraphAxis
from hud import HUD
from pigeon import Pigeon
from rifle import Rifle
from screen import PyGameScalableGraphScreen
from steps.boot_step import BootStep


class GameManager:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.clock = pygame.time.Clock()
        self.done = False

        self.screen = PyGameScalableGraphScreen("Tire au pigeon", 1600, 900, pygame.Color(100, 150, 200))

        self.pigeon = Pigeon("black", 5, 0, 20, 1000)
        self.rifle = Rifle("red", 5)

        self.screen.add_graph_line(self.pigeon)
        self.screen.add_graph_line(self.rifle)

        self.screen.add_axe(GraphAxis("width", "meters", "black", pygame.Color(89, 120, 180), 25, False))
        self.screen.add_axe(GraphAxis("height", "meters", "black", pygame.Color(89, 120, 180), 25, True))

        self.step = BootStep(self.rifle, self.pigeon)

        self.hud = HUD("Tire au pigeon d'argile", pygame.Color(25, 37, 50), pygame.Color(6, 8, 12),
                       pygame.Color(90, 130, 190), self.step)
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
            self.step.next_step().previous_step = self.step
            self.step = self.step.next_step()
            self.hud.step = self.step

    def handle_event(self, event):
        if event.type == pygame.QUIT:  # If user clicked close
            self.done = True  # Flag that we are done so we exit this loop

        self.step.handle_event(event)
        self.screen.handle_event(event)

    def get_playtime(self):
        return pygame.time.get_ticks() / 1000.0
