import threading
import time
import serial


class GeneralAndSyncPoolsThread(threading.Thread):
    def __init__(self,
        serialConnection,
        poolDelay: float = .2,
        activated: bool = True
        ):
        super().__init__()
        self.connection = serialConnection
        self.poolDelay = poolDelay
        self.activated = activated
    
    def run(self):
        while self.connection.is_open:
            try:
                if self.activated:
                    self.connection.write(b'\x80') # Sync
                    time.sleep(self.poolDelay)
                    self.connection.write(b'\x81') # General Pool
                    time.sleep(self.poolDelay)
                else:
                    time.sleep(self.poolDelay * 5)
            except serial.serialutil.PortNotOpenError as e:
                print("Synch exception - closing gp thread")
    
    def setDelay(newPoolDelay: float):
        self.poolDelay = newPoolDelay
    
    def activate():
        self.activate = True
    
    def deactivate():
        self.activate = False
            


