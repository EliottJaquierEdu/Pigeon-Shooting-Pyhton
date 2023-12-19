import pygame
from pygame.locals import *

from graph_line import GraphLine


class PyGameScalableGraphScreen:
    def __init__(self, caption, width, height, initial_graph_size=30):
        self.width = width
        self.height = height
        self.graph_size = initial_graph_size

        pygame.init()
        self.screen = pygame.display.set_mode([width, height], RESIZABLE)
        pygame.display.set_caption(caption)
        self.done = False
        self.clock = pygame.time.Clock()

        self.graph_lines = []
        self.force_lines_refresh = False

    def convert_vector_to_screen(self, vector):
        return [vector[0] * self.graph_size, self.height - vector[1] * self.graph_size]

    def add_graph_line(self, graph_line):
        self.graph_lines.append(graph_line)

    def update(self):
        while not self.done:
            for event in pygame.event.get():  # User did something
                self.handle_event(event)

            # Clear the screen and set the screen background
            self.screen.fill("white")

            for graph_line in self.graph_lines:
                lines = graph_line.get_lines(self.convert_vector_to_screen, self.force_lines_refresh)
                pygame.draw.lines(
                    self.screen, graph_line.color, False, lines, 5
                )
                for i in range(10):
                    pygame.draw.circle(self.screen, "blue", graph_line.get_point(i, self.convert_vector_to_screen), 7)

            self.force_lines_refresh = False

            # Go ahead and update the screen with what we've drawn.
            # This MUST happen after all the other drawing commands.
            pygame.display.flip()

        # Be IDLE friendly
        pygame.quit()

    def handle_event(self, event):
        if event.type == pygame.QUIT:  # If user clicked close
            self.done = True  # Flag that we are done so we exit this loop
        if event.type == pygame.VIDEORESIZE:
            self.width = event.w
            self.height = event.h
            self.force_lines_refresh = True
        if event.type == pygame.MOUSEWHEEL:
            self.graph_size += event.y*self.graph_size/10
