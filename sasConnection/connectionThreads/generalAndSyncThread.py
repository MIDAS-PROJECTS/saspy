import threading
import time
import serial


class GeneralAndSyncPoolsThread(threading.Thread):
    def __init__(self,
        serialConnection,
        commandBuffer: [bytes] = [],
        poolDelay: float = 2,
        activated: bool = True
        ):
        super().__init__()
        self.connection = serialConnection
        self.poolDelay = poolDelay
        self.activated = activated
        self.commandBuffer = commandBuffer
    
    def run(self):
        while self.connection.is_open:
            try:
                if self.activated:
                    self.connection.write(b'\x81') # Sync
                    time.sleep(self.poolDelay/2)
                    if self.commandBuffer:
                        cosa = self.commandBuffer.pop()
                        print(f"calling serial write to {cosa}")
                        self.connection.write(cosa)
                        #time.sleep(self.poolDelay/2)
                    self.connection.write(b'\x80') # General Pool
                    time.sleep(self.poolDelay/2)
            except serial.serialutil.PortNotOpenError as e:
                print("Synch exception - closing gp thread")
    
    def setDelay(newPoolDelay: float):
        self.poolDelay = newPoolDelay
    
    def activate():
        self.activate = True
    
    def deactivate():
        self.activate = False
            


