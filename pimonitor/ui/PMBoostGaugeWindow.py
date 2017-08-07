"""
Created on 22-04-2013

@author: citan
"""

import pygame
from pimonitor.cu.PMCUParameter import PMCUParameter


class PMBoostGaugeWindow(object):
    """
    classdocs
    """

    def __init__(self, parameter):
        self._fg_color = pygame.Color(255, 255, 255)
        self._fg_color_dim = pygame.Color(200, 140, 0)
        self._bg_color = pygame.Color(0, 0, 0)
        self._parameters = [parameter]
        self._packets = None


    def set_surface(self, surface):
        if surface is None:
            return

        parameter = self._parameters[0]

        self._surface = surface
        self._width = self._surface.get_width()
        self._height = self._surface.get_height()

        self._title_font_size = int(self._surface.get_height() / 12)
        self._value_font_size = int(self._surface.get_height() / 1.8)
        self._unit_font_size = int(self._surface.get_height() / 4)

        self._title_font = pygame.font.SysFont(pygame.font.get_default_font(), self._title_font_size)
        self._value_font = pygame.font.SysFont(pygame.font.get_default_font(), self._value_font_size)
        self._unit_font = pygame.font.SysFont(pygame.font.get_default_font(), self._unit_font_size)
	self._gauge_font = pygame.font.Font("pimonitor/resources/digital-7.ttf", 87)
        self._font_aa = 1

	self._needle = pygame.image.load("pimonitor/resources/needle.png").convert_alpha()
	self._background = pygame.image.load("pimonitor/resources/dial.png").convert_alpha()

        self._title_lbl = self._title_font.render(parameter.get_name(), self._font_aa, self._fg_color)

        self._unit_lbl = self._unit_font.render(parameter.get_default_unit(), self._font_aa, self._fg_color_dim)
        self._end_x_offset = self._width - self._unit_lbl.get_width() - 10
	self._needleX = self._width / 2
	self._needleY = self._height / 2
	self._dial1X = self._width / 2
	self._dial1Y = 450
	self._backgroundX = 262
	self._backgroundY = 50


    def render(self):
        value = 0.0
        parameter = self._parameters[0]
        if self._packets is not None:
                value = float(parameter.get_calculated_value(self._packets))

	displayValue = self._gauge_font.render(("%s" % value), 1, (241,241,241))
	labelRect = displayValue.get_rect()
        labelRect.centerx = self._dial1X
        labelRect.centery = self._dial1Y

	needleNew = pygame.transform.rotate(self._needle, (40 - (value * 8)))
	needle_rect = needleNew.get_rect()
	needle_rect.center = (self._needleX, self._needleY)

	self._surface.blit(self._title_lbl, (2, 2))
	self._surface.blit(self._background, (self._backgroundX, self._backgroundY))
        self._surface.blit(needleNew, needle_rect)
        self._surface.blit(displayValue, (labelRect))

    def set_packets(self, packets):
        self._packets = packets

    def get_parameters(self):
        return self._parameters
