import bcd
import serial
import sys
import binascii

class SasConnection():

    def __init__(self, port):

        try:
            self.connection = serial.Serial(port=port, baudrate=19200, timeout=2)
        except:
            print("Serial connection error")
            sys.exit()
    

    def start(self):
        print("Initializing SAS connection")
        while True:
            response = self.connection.read(1)
            if response( != ''):
                self.adress = int(binascii)
