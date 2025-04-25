import serial
import sys
import binascii
import time

from PyCRC.CRC16Kermit import CRC16Kermit

import utilities.stateGenerators as gens

class SasConnection():

    def __init__(self, port:str, address:int):

        self.port = port
        self.address = address
        self.meters = gens.genMeters()
    
    def connect(self):
        try:
            self.connection = serial.Serial(port = self.port,
                                                baudrate = 19200,
                                                timeout = 2)
        except serial.SerialException as e:
            raise e
        except Exception as e:
            raise e
    

    def start(self):
        print("Initializing SAS connection")
        while True:
            response = self.connection.read(1)
            if response != '':
                readAddress = int(binascii.hexlify(response))
                if self.address == readAddress:
                    print(f"valid address recognized: {self.address}")
                    break
            
            time.sleep(.5)
        
        self.machineIDAndInformation()
    
    def stop(self):
        self.connection.close()
        

    
    def machineIDAndInformation(self):
        #1F
        cmd = [0x1F]
        data = self.__sendCommand(cmd, True, crc_need = False)
        if data != '':
            self.meters['ASCII_game_ID'] = data[1:3].decode(errors='ignore')
            self.meters['ASCII_additional_ID'] = data[3:6].decode(errors='ignore')
            self.meters['bin_denomination'] = self.__from_bcd(data[6:7])
            self.meters['bin_max_bet'] = self.__from_bcd(data[7:8])
            self.meters['bin_progressive_mode'] = self.__from_bcd(data[8:9])
            self.meters['bin_game_options'] = self.__from_bcd(data[9:11])
            self.meters['ASCII_paytable_ID'] = data[11:17].decode(errors='ignore')
            self.meters['ASCII_base_percentage'] = data[17:21].decode(errors='ignore')
    
    def meters_11_15(self):
        #19
        cmd = [0x19]
        data = self.__sendCommand(cmd, True, crc_need = False)
        if data != '':
            self.meters['total_bet_meter'] = self.__from_bcd(data[1:5])
            self.meters['total_win_meter'] = self.__from_bcd(data[5:9])
            self.meters['total_in_meter'] = self.__from_bcd(data[9:13])
            self.meters['total_jackpot_meter'] = self.__from_bcd(data[13:17])
            self.meters['games_played_meter'] = self.__from_bcd(data[17:21])


    def __sendCommand(self, command, no_response=False, timeout=3, crc_need=True):
        response = b''
        try:
            packet = bytearray([self.address] + command)
            if crc_need:
                crc= self.__calculate_crc(packet)
                packet.extend([(crc >> 8) & 0xFF, crc & 0xFF])
            
            print(f"Sending: {binascii.hexlify(packet)}")
            self.connection.write(packet)

            if no_response:
                return b''
            
            self.connection.reset_input_buffer()
            start_time = time.time()

            while time.time() - start_time < timeout:
                response += self.connection.read(1)
                parsed = self.checkResponse(response)
                if parsed:
                    return parsed
            
            print("Timeout waiting for response")
            return None
        except Exception as e:
            print(f"Error in __sendCommand: {e}")
            return None
            
    

    def __calculate_crc(self, data_bytes):
        return CRC16Kermit().calculate(data_bytes)
    
    def checkResponse(self, rsp):
        if not rsp:
            return False

        resp = bytearray(rsp)
        if resp[0] != self.address:
            raise ValueError(f"Unexpected address: {resp[0]} (expected {self.address})")

        received_crc = resp[-2:]
        data = resp[1:-2]
        crc_calc = self.__calculate_crc(resp[:-2])

        crc_bytes = bytearray([(crc_calc >> 8) & 0xFF, crc_calc & 0xFF])

        if received_crc != crc_bytes:
            print(f"CRC mismatch: received {binascii.hexlify(received_crc)}, expected {binascii.hexlify(crc_bytes)}")
            return False

        return data
    
    def __from_bcd(self, data):
        return int(binascii.hexlify(data),16)


