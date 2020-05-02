import serial #Import Serial Library

global ser
ser = serial.Serial()
ser.port = 'COM8'
ser.baudrate = 9600
#ser.timeout = 0

#arduinoSerialData = serial.Serial('com8',9600) #Create Serial port object called arduinoSerialData
if ser.isOpen() == False:
     ser.open()
 
while (1==1):
    if (ser.inWaiting()>0):
        myData = ser.readline().decode("utf-8")
        print(myData)