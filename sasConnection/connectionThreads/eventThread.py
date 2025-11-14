import threading
import time
from utilities.generalExceptionCodes import ExceptionCodes

from types import FunctionType



class EventThread(threading.Thread):
    def __init__(self,
    readBuffer: [bytes],
    exceptionLogFunc : FunctionType,
    commandLogFunc : FunctionType,
    commandBuffer: [bytes] = [] #This is put as empty because lol
    ):
        super().__init__()
        self.readBuffer = readBuffer
        self.commandBuffer = commandBuffer
        self.Cont = True
        self.exceptionLogFunc = exceptionLogFunc
        self.commandLogFunc = commandLogFunc
    
    def run(self):
        while self.Cont:
            if self.readBuffer:
                self.analyzeFullInput(self.readBuffer.pop())
            time.sleep(.05)

    
    def analyzeFullInput(self, fullInput: bytes):
        #TODO: should use commandBuffer to know if a command is pending to be read
        #separatedInput = fullInput.split(b'\x01') #The parameter of split should be the direction I guess
        #for input in separatedInput:
        self.analyzeInput(fullInput)
    
    def analyzeInput(self, input:bytes):
        if len(input) == 1:
            self.handleGeneralException(input)
        elif len(input) > 1:
            #TODO: manejo de respuestas de longitudes mas grandes
            #self.commandLogFunc("respuesta de muchos ACKS o a un comando")
            self.commandLogFunc(f"{input}")
    

    def handleGeneralException(self, input: bytes):
        #TODO: this should push a notification or something different
        try:
            exceptionResult = ExceptionCodes(input)
            self.exceptionLogFunc(f"${exceptionResult.value} - {exceptionResult.name}")
        except ValueError as ve:
                self.exceptionLogFunc(f"${input} - Unknown exception code read")
    
    def stopExcecution(self):
        self.Cont = False
    

