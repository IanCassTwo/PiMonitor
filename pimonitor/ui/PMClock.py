"""
Created on 22-04-2013

@author: citan
"""

import pygame
import time
from time import gmtime, strftime
from pimonitor.cu.PMCUParameter import PMCUParameter


class PMClock():
    """
    classdocs
    """

    def __init__(self):
        self._fg_color = pygame.Color(255, 255, 255)
        self._fg_color_dim = pygame.Color(215, 215, 215)
        self._bg_color = pygame.Color(0, 0, 0)

        self._x_offset = 0
        self._sum_value = 0.0
        self._readings = 0

    def set_surface(self, surface):
        if surface is None:
            return

        self._surface = surface
        self._width = self._surface.get_width()
        self._height = self._surface.get_height()

        self._title_font_size = int(self._surface.get_height() / 12)
        self._value_font_size = int(self._surface.get_height() / 1.8)
        self._unit_font_size = int(self._surface.get_height() / 4)

        self._title_font = pygame.font.SysFont(pygame.font.get_default_font(), self._title_font_size)
        self._value_font = pygame.font.SysFont(pygame.font.get_default_font(), self._value_font_size)
        self._unit_font = pygame.font.SysFont(pygame.font.get_default_font(), self._unit_font_size)

        self._font_aa = 1

	self._title_lbl = self._title_font.render("Current Time", self._font_aa, self._fg_color)

    def render(self):
        value = strftime("%H:%M", gmtime());
	year = strftime("%B %Y", gmtime());

        value_lbl_width = self._value_font.render(value, self._font_aa, self._fg_color).get_width()
        self._x_offset = (self._width - value_lbl_width) / 2
        value_lbl = self._value_font.render(value, self._font_aa, self._fg_color)

	avg_value_lbl = self._unit_font.render(year, self._font_aa, self._fg_color_dim)
	self._surface.blit(avg_value_lbl, ((self._x_offset + value_lbl_width) - avg_value_lbl.get_width(), 10 + self._title_lbl.get_height() + value_lbl.get_height()))

        self._surface.blit(self._title_lbl, (2, 2))
        self._surface.blit(value_lbl, (self._x_offset, 10 + self._title_font_size))


    def set_packets(self, packets):
        self._packets = packets

    def get_parameters(self):
        return 
