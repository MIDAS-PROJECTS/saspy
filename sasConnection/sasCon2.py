import serial
import sys
import time
import threading

from types import FunctionType

import utilities.stateGenerators as gens

from sasConnection.connectionThreads import EventThread, GeneralAndSyncPoolsThread, ReaderThread


class SasConnection():

    def __init__(self, port: str, address: int, exceptionLogFunc = print, commandLogFunc = print):
        self.__setup(port = port,
            address = address,
            exceptionLogFunc = exceptionLogFunc,
            commandLogFunc = commandLogFunc
        )
    
    def connect(self):
        try:
            print("Init serial connection...")
            self.connection = serial.Serial(
                port = self.port,
                baudrate = 19200, #look how to change this to a constant in serial
                timeout = 2)
            self.__createThreads()
            self.__startThreads()
            
        except serial.SerialException as e:
            print("Connection error")
            raise e
        except Exception as e:
            print("Unkown exception raised")
            raise e
    
    def __setup(self, port: str, address: int, exceptionLogFunc : FunctionType, commandLogFunc: FunctionType):
        self.port : str = port
        self.address : int = address
        self.meters : dict = gens.genMeters()
        self.connection : serial.Serial = None
        self.__readBuffer : [bytes] = []
        self.__commandBuffer : [bytes] = []
        self.__exceptionLogFunc : FunctionType = exceptionLogFunc
        self.__commandLogFunc : FunctionType = commandLogFunc

    def __createThreads(self):
        self.__eventThread = EventThread(self.__readBuffer,
            self.__commandBuffer,
            self.__exceptionLogFunc,
            self.__commandLogFunc
        )
        self.__gpSyncThread = GeneralAndSyncPoolsThread(self.connection)
        self.__readerThread = ReaderThread(self.connection, self.__readBuffer)
    
    def __startThreads(self):
        self.__eventThread.start()
        self.__gpSyncThread.start()
        self.__readerThread.start()
    
    def __joinThreads(self):
        self.__eventThread.join()
        self.__gpSyncThread.join()
        self.__readerThread.join()
    
    def stop(self):
        self.__eventThread.stopExcecution()
        self.connection.close()
        self.__joinThreads()


