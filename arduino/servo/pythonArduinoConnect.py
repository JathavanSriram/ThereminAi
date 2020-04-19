# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 13:17:17 2020

@author: Julian

This program is communicating with the Arduino board steering the servo.
It contains the functions to setup the pins, the connection COMS and steering the servo using speed and position as a variable.
The program uses a config file to read out the connection Pins and COMS.

Contained functions:
      setupPins()
      setupCOMs()
      steerServo()
      
Connected files:
      configPyArd.txt
"""

#main