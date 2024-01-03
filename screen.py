import pygame
from pygame.locals import *


class PyGameScalableGraphScreen:
    def __init__(self, caption, width, height, initial_graph_size=30):
        self.width = width
        self.height = height

        self.screen = pygame.display.set_mode([width, height], RESIZABLE)
        pygame.display.set_caption(caption)

        self.graph_lines = []
        self.axes = []
        self.force_lines_refresh = False
        self.dragging = False
        self.graph_size = initial_graph_size
        self.offset = [0, 0]
        self.last_mouse_position = [0, 0]

    def convert_vector_to_screen(self, vector):
        return [vector[0] * self.graph_size + self.offset[0], self.height - vector[1] * self.graph_size + self.offset[1]]

    def convert_screen_to_vector(self, screen_vector):
        return [(screen_vector[0] - self.offset[0]) / self.graph_size, (screen_vector[1] - self.offset[1]) / self.graph_size]

    def add_graph_line(self, graph_line):
        self.graph_lines.append(graph_line)

    def add_axe(self,axe):
        self.axes.append(axe)

    def render(self):
        # Clear the screen and set the screen background
        self.screen.fill(pygame.Color(100, 150, 200))

        for graph_line in self.graph_lines:
            lines = graph_line.get_lines(self.convert_vector_to_screen, self.force_lines_refresh)
            pygame.draw.lines(
                self.screen, graph_line.color, False, lines, 5
            )
            for i in range(10):
                pygame.draw.circle(self.screen, "blue", graph_line.get_point(i, self.convert_vector_to_screen), 7)

        self.force_lines_refresh = False

        infos = self.get_chunks_resolution_infos()

        for axe in self.axes:
            axe.draw(self.screen, self.width, self.height, self.offset[0], self.offset[1], infos[0], infos[1])

    def get_chunks_resolution_infos(self):
        mantissa = self.graph_size
        mantissa = mantissa / 3
        multiplier = 1
        while mantissa > 10:
            mantissa /= 10
            multiplier *= 10
        while mantissa < 1:
            mantissa *= 10
            multiplier /= 10
        mantissa = mantissa * 3
        return [mantissa * 10, multiplier]

    def handle_event(self, event):
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
