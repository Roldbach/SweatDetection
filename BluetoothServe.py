import serial

from Configuration import bluetoothConfiguration

class BluetoothServe:
    '''
        The class to enable bluetooth communication between Arduino
    and PC
    '''
    def __init__(self):
        self.port=bluetoothConfiguration["port"]
        self.baud=bluetoothConfiguration["baud rate"]
        self.serial=None
        self.status=False
    
    def connect(self):
        '''
            Connect to the arduino and set the status according to the connection
        '''
        try:
            self.serial=serial.Serial(self.port, self.baud)
            self.serial.flushInput()
            self.status=True
        except:
            self.status=False
    
    def read(self):
        '''
            Read the data from arduino and decode into String type for further use
        '''
        try:
            result=self.serial.readline().decode("utf-8")
            return result.strip("\r\n")
        except:
            return "Error"
        
    def write(self, command="H"):
        '''
            Write commands to the arduino

            The following commands could be generated:
            (1) Alarm (LED blinking + active buzzer beeping)
        '''
        try:
            self.serial.write(bytes(command, "utf-8"))
            return True
        except:
            return False
    
    def close(self):
        try:
            self.serial.close()
            return True
        except:
            return False    
    
