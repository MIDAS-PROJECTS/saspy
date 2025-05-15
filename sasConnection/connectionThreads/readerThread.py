
import threading
import time
import serial

class ReaderThread(threading.Thread):
    def __init__(self,
    serialConnection,
    readBuffer: [bytes],
    readDelay: float = .1,
    ):
        super().__init__()
        self.connection = serialConnection
        self.readBuffer = readBuffer
        self.readDelay = readDelay
        
    def run(self):
        while self.connection.connection.is_open:
            self.readBuffer.append(self.connection.read(self.connection.in_waiting))
            time.sleep(self.readDelay)
    
    def setDelay(newReadDelay: float):
        self.readDelay = newReadDelay
