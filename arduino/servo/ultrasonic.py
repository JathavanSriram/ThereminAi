import serial #Import Serial Library
 
arduinoSerialData = serial.Serial('com8',9600) #Create Serial port object called arduinoSerialData
 
 
while (1==1):
    if (arduinoSerialData.inWaiting()>0):
        myData = arduinoSerialData.readline()
        print(myData)