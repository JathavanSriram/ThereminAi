# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 21:41:30 2020

@author: Julian
"""
#This program drives the servo to follow a angle sequence, hence a tone sequenc with variable timing
import serial
import time

freqArray=[48,170,90]

def initialize():
      ser.write(bytes([80]))
      time.sleep(1)

def fitFreq(target):
      global ser
      ser.write(bytes([target]))
      
#main
global ser
ser = serial.Serial()
ser.port = 'COM8'
ser.baudrate = 9600
ser.timeout = 0
# open port if not already open
if ser.isOpen() == False:
      ser.open()

initialize()
for i in range (4):
      fitFreq(freqArray[i-1])
      time.sleep(1)