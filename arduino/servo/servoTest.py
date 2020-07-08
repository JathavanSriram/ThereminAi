# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 21:41:30 2020

@author: Julian
"""
#This program drives the servo to follow a angle sequence, hence a tone sequenc with variable timing
import serial
import time


# TODO: Pending documentation on functions


def initialize(ser):

      ser.write(bytes([80]))
      time.sleep(1)

def fitFreq(ser,target):

      if target < 48:
            target = 48
      elif target > 170:
            target = 170
            
      ser.write(bytes([target]))


def main():

      ser = serial.Serial()
      ser.port = '/dev/ttyACM0'
      ser.baudrate = 9600
      ser.timeout = 0
      
      freqArray=[48,170,170,48,90]


      # open port if not already open
      if ser.isOpen() == False:
            ser.open()

      initialize(ser)

      for i in range (6):
            fitFreq(ser,freqArray[i-1])
            time.sleep(1)



if __name__ == "__main__":
      main()