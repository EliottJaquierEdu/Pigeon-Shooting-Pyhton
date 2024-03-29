import pygame
from pygame.locals import *


class PyGameScalableGraphScreen:
    def __init__(self, caption, width, height, background_color, initial_graph_size=30):
        self.width = width
        self.height = height
        self.background_color = background_color

        self.screen = pygame.display.set_mode([width, height], RESIZABLE)
        pygame.display.set_caption(caption)

        self.drawable_objects = []
        self.axes = []
        self.ui = []

        self.dragging = False
        self.graph_size = initial_graph_size
        self.offset = [0, 0]
        self.last_mouse_position = [0, 0]

    def convert_vector_to_screen(self, vector):
        return [vector[0] * self.graph_size + self.offset[0],
                self.height - vector[1] * self.graph_size + self.offset[1]]

    def convert_screen_to_vector(self, screen_vector):
        return [(screen_vector[0] - self.offset[0]) / self.graph_size,
                ((self.height - screen_vector[1]) + self.offset[1]) / self.graph_size]

    def add_drawable_object(self, graph_line):
        self.drawable_objects.append(graph_line)

    def add_ui(self, ui):
        self.ui.append(ui)

    def add_axe(self, axe):
        self.axes.append(axe)

    def clear(self):
        self.screen.fill(self.background_color)

    def render(self):
        for drawable_object in self.drawable_objects:
            drawable_object.draw(self.screen, self.width, self.height, self.convert_vector_to_screen)

        infos = self.get_chunks_resolution_infos()
        for axe in self.axes:
            axe.draw(self.screen, self.width, self.height, self.offset[0], self.offset[1], infos[0], infos[1])

        for ui in self.ui:
            ui.draw(self.screen, self.width, self.height)

        pygame.display.flip()

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
        if event.type == pygame.MOUSEWHEEL:
            last_graph_size = self.graph_size
            size_delta = event.y * self.graph_size / 10
            self.graph_size += size_delta
            delta = self.graph_size / last_graph_size

            center_point = [(self.width / 2), (self.height / 2)]

            self.offset[0] = (self.offset[0] - center_point[0]) * delta + center_point[0]
            self.offset[1] = (self.offset[1] + center_point[1]) * delta - center_point[1]
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
