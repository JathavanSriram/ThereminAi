# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 21:41:30 2020

@author: Julian
"""
#This program drives the servo to follow a angle sequence, hence a tone sequenc with variable timing
import serial
import time
"""import socket
import threading
import sys

#Wait for incoming data from server
#.decode is used to turn the message in bytes to a string
def receive(socket, signal):
    while signal:
        try:
            data = socket.recv(32)
            print(str(data.decode("utf-8")))
        except:
            print("You have been disconnected from the server")
            signal = False
            break"""


freqArray=[48,170,170,48,90]

def initialize():
      ser.write(bytes([80]))
      time.sleep(1)

def moveServo(target):
      global ser
      if target < 48:
            target = 48
      elif target > 170:
            target = 170
            
      ser.write(bytes([target]))
      
def fitServo(ser,target,angleTemp):
      myData = (ser.readline().decode("utf-8"))
      moveServo(angleTemp)
      print(myData)
      distTemp = int(myData)
      
      if distTemp-target > 0:
            angleTemp -=5
            return(angleTemp)
      elif distTemp-target < 0:
            angleTemp +=5
            return(angleTemp)
            
      else:
            print("in Target")
            return(angleTemp)

      
#main----------------
global ser
ser = serial.Serial()
ser.port = 'COM8'
ser.baudrate = 9600
#ser.timeout = 0
# open port if not already open
if ser.isOpen() == False:
      ser.open()

initialize()

target = 10
angleTemp = 90

"""#Get host and port
host = "192.168.1.2"
port = 24000

#Attempt connection to server
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
except:
    print("Could not make a connection to the server")
    input("Press enter to quit")
    sys.exit(0)

#Create new thread to wait for data
receiveThread = threading.Thread(target = receive, args = (sock, True))
receiveThread.start()"""

while True:
      if (ser.inWaiting()>0):
            angleTemp = fitServo(ser,target,angleTemp)
            moveServo(angleTemp)
        
      time.sleep(0.4)