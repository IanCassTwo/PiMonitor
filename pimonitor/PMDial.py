# -*- coding: utf-8 -*-

"""
Created on 29-03-2013

@author: citan
"""

import os
import os.path
import time
import cPickle as pickle
import platform
import re
import sys
import pygame

from pimonitor.PM import PM
from pimonitor.PMConnection import PMConnection
from pimonitor.PMDemoConnection import PMDemoConnection
from pimonitor.PMXmlParser import PMXmlParser
from pimonitor.cu.PMCUParameter import PMCUParameter
from pimonitor.cu.PMCUContext import PMCUContext
from pimonitor.ui.PMScreen import PMScreen
from pimonitor.ui.PMSingleWindow import PMSingleWindow
from pimonitor.ui.PMWindow import PMWindow
from pimonitor.ui.PMBoostGaugeWindow import PMBoostGaugeWindow
from pimonitor.ui.PMClock import PMClock
from pygame.locals import *


def stringSplitByNumbers(x):
    r = re.compile('(\d+)')
    l = r.split(x.get_id())
    return [int(y) if y.isdigit() else y for y in l]


if __name__ == '__main__':

    pygame.init()

    size = width, height = 1024, 600

    #pygame.display.set_caption('K11Consult: %s' % __file__)

    monitorX = pygame.display.Info().current_w
    monitorY = pygame.display.Info().current_h

    screen = pygame.display.set_mode((monitorX,monitorY), FULLSCREEN)
    fontEco = pygame.font.Font("pimonitor/resources/Teko-Regular.ttf", 60)

    if platform.system() == "Linux":
        from evdev import InputDevice, list_devices

        devices = map(InputDevice, list_devices())
        eventX = ""
        for dev in devices:
            print dev.name
            if dev.name == "ft5x_ts":
                eventX = dev.fn

    os.environ["SDL_FBDEV"] = "/dev/fb1"
    os.environ["SDL_MOUSEDRV"] = "TSLIB"
    os.environ["SDL_MOUSEDEV"] = eventX


    screen = PMScreen()
    screen.render()

    parser = PMXmlParser()

    supported_parameters = []

    if os.path.isfile("data/data.pkl"):
        serializedDataFile = open("data/data.pkl", "rb")
        defined_parameters = pickle.load(serializedDataFile)
        serializedDataFile.close()
    else:
        defined_parameters = parser.parse("logger_IMP_EN_v323.xml")
        defined_parameters = sorted(defined_parameters, key=lambda x: x.get_id(), reverse=True)
        output = open("data/data.pkl", "wb")
        pickle.dump(defined_parameters, output, -1)
        output.close()

    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        connection = PMDemoConnection()
    elif platform.system() == "Linux":
        connection = PMConnection()
    else:
        connection = PMDemoConnection()

    while True:
        try:
            connection.open()
            ecu_packet = connection.init(1)

            ecu_context = PMCUContext(ecu_packet, [1, 3])
            ecu_parameters = ecu_context.match_parameters(defined_parameters)
            ecu_switch_parameters = ecu_context.match_switch_parameters(defined_parameters)
            ecu_calculated_parameters = ecu_context.match_calculated_parameters(defined_parameters, ecu_parameters)

            supported_parameters = ecu_parameters + ecu_switch_parameters + ecu_calculated_parameters

            supported_parameters = sorted(supported_parameters, key=stringSplitByNumbers)

            # Build our screens & data sources
            # Clock first
            screen.add_window(PMClock())

	    pids = ["P1", "P2", "P9", "P11", "P202", "P58", "P203"]
            parameters = {}
            for parameter in supported_parameters:
		# Boost
                if parameter.get_id() == "P202":
			window = PMBoostGaugeWindow(parameter)
			screen.add_window(window)

		# ECO switch
                #if parameter.get_id() == "S108":
		#	parameters[parameter.get_id()] = parameter;

		# Others
		if parameter.get_id() in pids:
			window = PMSingleWindow(parameter)
			screen.add_window(window)

            # Schedule our events
            pygame.time.set_timer(USEREVENT + 1, 500)

            eco_text = ""

            screen.next_window()

            while True:

		window = screen.get_window()
                window_parameters = window.get_parameters()

                # TODO refactor - not possible to test at the moment, so leave working part untouched
                if window_parameters is not None: 
			if len(window_parameters) == 1:
			    parameter = window_parameters[0]
			    if parameter.get_cu_type() == PMCUParameter.CU_TYPE_STD_PARAMETER():
				packet = connection.read_parameter(parameter)
				window.set_packets([packet])
			    elif parameter.get_cu_type() == PMCUParameter.CU_TYPE_FIXED_ADDRESS_PARAMETER():
				packet = connection.read_parameter(parameter)
				window.set_packets([packet])
			    elif parameter.get_cu_type() == PMCUParameter.CU_TYPE_SWITCH_PARAMETER():
				packet = connection.read_parameter(parameter)
				window.set_packets([packet])
			    elif parameter.get_cu_type() == PMCUParameter.CU_TYPE_CALCULATED_PARAMETER():
				packets = connection.read_parameters(parameter.get_dependencies())
				window.set_packets(packets)
			elif len(window_parameters) > 1:
			    packets = connection.read_parameters(window_parameters)
			    window.set_packets(packets)

		# Handle events
		# TODO move eco switch stuff elsewhere
                #for event in pygame.event.get():

			# 1 sec tick
			#if event.type==pygame.USEREVENT + 1:
			#	# eco switch
			#	parameter = parameters["S108"]
                        #	packet = connection.read_parameter(parameter)
			#	if parameter.get_value(packet) == "1":
			#		eco_text = "ECO"
			#	else:
			#		eco_text = ""
				
				
		# eco switch
		#ecoValue = fontEco.render(("%s" % eco_text), 1, (0,255,0))
		#ecoRect = ecoValue.get_rect()
		#ecoRect.centerx = 980
		#ecoRect.centery = 30

		#screen.fill(0x000000)
		#screen.blit(ecoValue, (ecoRect))

		screen.render()


        except IOError as e:
            if connection is not None:
                connection.close()
                time.sleep(3)
            continue

