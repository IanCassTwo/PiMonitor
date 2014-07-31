"""
Created on 29-03-2013

@author: citan
"""
from pimonitor.PM import PM
from pimonitor.PMPacket import PMPacket
import random
import time


class PMDemoConnection(object):

    def __init__(self):
        self._ser = None
        self._log_id = None
        random.seed()
    
        self._byteval = [0, 0, 0, 0]

    def open(self):
        message = 'Opening serial connection...'
        self._log_id = PM.log(message)
        time.sleep(0.2)
        PM.log(message + " [DONE]", self._log_id)

        return True

    def close(self):
        PM.log("Closing serial connection", self._log_id)
        pass
        
    def init(self, target):
        PM.log('Initializing CU for target: ' + str(target), self._log_id)
        response = []
        if target == 1 or target == 3:
            response = [0x80, 0xF0, 0x10, 0x69, 0xFF, 0xA2, 0x10, 0x02, 0x4D, 0x12, 0x04, 0x40, 0x06, 0xF3, 0xFA, 0xC9, 0x8E, 0x22, 0x04, 0x02, 0xAC, 0x00, 0x00, 0x00, 0x60, 0xCE, 0x54, 0xF8, 0xB9, 0x84, 0x00, 0x6C, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0xDC, 0x00, 0x00, 0x45, 0x1F, 0x30, 0x80, 0xF0, 0x20, 0x1F, 0x02, 0x43, 0xFB, 0x00, 0xF1, 0xC1, 0x84, 0x00, 0x00, 0x00, 0x00, 0x00, 0xF1, 0x80, 0x00, 0x00, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x26]
        if target == 2:
            response = [0x80, 0xF0, 0x18, 0x39, 0xFF, 0xA2, 0x10, 0x21, 0xD0, 0xF3, 0x70, 0x31, 0x00, 0x01, 0x00, 0x80, 0x04, 0x00, 0x00, 0x00, 0x00, 0xBD, 0xC3, 0xC0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x49, 0x3E, 0x00, 0x0B, 0x21, 0xC0, 0x00, 0x00, 0x01, 0x1F, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x51]
            
        return PMPacket.from_array(response)

    def read_parameter(self, parameter):
        time.sleep(0.05)
        address_len = parameter.get_address().get_length()

        data = [0x80, 0xF0]  # [0x80, 0xF0, 0x18, 0x02, 0xE8, 0x60, 0xD2]

        if parameter.get_target() == 1 or parameter.get_target() == 3:
            data.append(0x10) 
        if parameter.get_target() == 2:
            data.append(0x18) 
 
        data.append(address_len+1)
        data.append(0xE8)
        
        for i in range(0, address_len):
            self._byteval[i] = (self._byteval[i] + 1) % 0xFF
            data.append(self._byteval[i])
        
        checksum = 0
        for b in data:
            checksum = (checksum + b) & 0xFF

        data.append(checksum)

        return PMPacket.from_array(data)
    
    def read_parameters(self, parameters):
        time.sleep(0.05)
        out_packets = []
        
        for parameter in parameters:
            out_packets.append(self.read_parameter(parameter))
            
        return out_packets
