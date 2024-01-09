import pygame

from objects.graph_axis import GraphAxis
from hud import HUD
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

        sky = pygame.Color(43, 149, 199)
        blue = pygame.Color(31, 114, 153)
        dark = pygame.Color(12, 43, 57)
        hud = pygame.Color(25, 95, 128)
        hud = pygame.Color(102,172,204)
        title = pygame.Color(25, 37, 50)
        text = pygame.Color(10, 38, 51)
        ground = pygame.Color(75, 29, 4)

        self.screen = PyGameScalableGraphScreen("Tire au pigeon", 1600, 900, sky)

        self.pigeon = Pigeon(dark, 5, 0, 20, 1000)
        self.rifle = Rifle(dark, 5)
        self.ground = Ground(ground)

        self.screen.add_drawable_object(self.ground)
        self.screen.add_drawable_object(self.pigeon)
        self.screen.add_drawable_object(self.rifle)

        self.screen.add_axe(GraphAxis("width", "meters", dark, blue, 25, False))
        self.screen.add_axe(GraphAxis("height", "meters", dark, blue, 25, True))

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
