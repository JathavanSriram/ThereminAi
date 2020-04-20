# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 21:41:30 2020

@author: Julian
"""
#This program drives the servo to follow a angle sequence, hence a tone sequenc with variable timing
import serial
import time

freqArray=[20,20,20,40,110,110,70,50,55,10,175,175,170,170,25]

def initialize():
      ser.write(bytes([90]))
      time.sleep(5)

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
for i in range (15):
      fitFreq(freqArray[i])
      time.sleep(0.5)