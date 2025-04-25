import bcd
import serial
import sys
import binascii
import time

from PYCRC.CRC16Kermit import CRC16Kermit
from array import array

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
        data = self.__sendCommand(cmd, true, crc_need = False)
        if data != '':
            self.meters['ASCII_game_ID']=(((data[1:3])))
            self.meters['ASCII_additional_ID']=(((data[3:6])))
            self.meters['bin_denomination']=int(binascii.hexlify(bytearray(data[6])))
            self.meters['bin_max_bet']=(binascii.hexlify(bytearray(data[7:8])))
            self.meters['bin_progressive_mode']=int(binascii.hexlify(bytearray(data[8:9])))
            self.meters['bin_game_options']=(binascii.hexlify(bytearray(data[9:11])))
            self.meters['ASCII_paytable_ID']=(((data[11:17])))
            self.meters['ASCII_base_percentage']=(((data[17:21])))
    
    def meters_11_15(self):
        #19
        cmd = [0x19]
        data = self.__sendCommand(cmd, True, crc_need = False)
        if data != '':
            self.meters['total_bet_meter']=int(binascii.hexlify(bytearray(data[1:5])))
            self.meters['total_win_meter']=int(binascii.hexlify(bytearray(data[5:9])))
            self.meters['total_in_meter']=int(binascii.hexlify(bytearray(data[9:13])))
            self.meters['total_jackpot_meter']=int(binascii.hexlify(bytearray(data[13:17])))
            self.meters['games_played_meter']=int(binascii.hexlify(bytearray(data[17:21])))


    def __sendCommand(self, command, no_response=False, timeout=3, crc_need=True):
        busy = True
        response = b''
        try:
            buf_header = [self.address]
            buf_header.extend(command)
            buf_count = len(command)

            if (crc_need):
                crc=CRC16Kermit().calculate(str(bytearray(buf_header)))
                buf_header.extend([((crc>>8)&0xFF),(crc&0xFF)])
            
            print(buf_header)

            self.connection.write((buf_header))
        
        except Exception as e:
            print(e)
        
        try:
            buffer = []
            self.connection.flushInput()
            t = time.time()
            while time.time() - t<timeout:
                response += self.connection.read()

                if self.checkResponse != False:
                    break
            
            if time.time() - t >= timeout:
                print("timeout waiting response")
                return None
            busy = False
            return self.checkResponse(response)
        
        except Exception as e:
            print(e)
        busy = False
        return None
    
    def checkResponse(self, rsp):
        if (rsp==''):
            return False
        resp = bytearray(rsp)

        if (resp[0] != self.address):
            raise Exception("incorrect adress catched in serial connection")
        
        CRC = binascii.hexlify(resp[-2:])

        command = resp[0:-2]

        crc1=crc=CRC16Kermit().calculate(str(bytearray(command)))

        data = resp[1:-2]

        crc1 = hex(crc1).split('x')[-1]

        while len(crc1)<4:
                        crc1 = "0"+crc1
        
        if CRC != crc1:
            return False
        
        return data


