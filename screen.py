import math

import pygame
from pygame.locals import *

from graph_line import GraphLine


class PyGameScalableGraphScreen:
    def __init__(self, caption, width, height, initial_graph_size=30):
        self.width = width
        self.height = height

        pygame.init()
        self.screen = pygame.display.set_mode([width, height], RESIZABLE)
        pygame.display.set_caption(caption)
        self.done = False
        self.clock = pygame.time.Clock()

        self.graph_lines = []
        self.force_lines_refresh = False
        self.dragging = False
        self.graph_size = initial_graph_size
        self.offset = [0, 0]
        self.last_mouse_position = [0, 0]

    def convert_vector_to_screen(self, vector):
        return [vector[0] * self.graph_size + self.offset[0],
                self.height - vector[1] * self.graph_size + self.offset[1]]

    def add_graph_line(self, graph_line):
        self.graph_lines.append(graph_line)

    def update(self):
        while not self.done:
            for event in pygame.event.get():  # User did something
                self.handle_event(event)

            # Clear the screen and set the screen background
            self.screen.fill("white")

            rifle = self.graph_lines[1]
            start_rifle_point = rifle.get_point(0, self.convert_vector_to_screen)
            mousePosition = pygame.mouse.get_pos()
            mouseRelativePosition = [mousePosition[0] - start_rifle_point[0],mousePosition[1] - start_rifle_point[1]]
            angle = -math.atan2(mouseRelativePosition[1], mouseRelativePosition[0])
            rifle.angle = math.degrees(angle)
            if rifle.angle < 0:
                rifle.angle = 180 if rifle.angle < -90 else 0

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
            self.graph_size += event.y * self.graph_size / 10
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.dragging = True
            self.last_mouse_position = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        if event.type == pygame.MOUSEMOTION:
            if not self.dragging:
                return
            delta_x = event.pos[0] - self.last_mouse_position[0]
            delta_y = event.pos[1] - self.last_mouse_position[1]
            self.last_mouse_position = event.pos
            self.offset[0] += delta_x
            self.offset[1] += delta_y
