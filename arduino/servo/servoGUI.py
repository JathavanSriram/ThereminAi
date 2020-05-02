# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 21:59:47 2020

@author: Julian
"""

# -*- coding: utf-8 -*-
from tkinter import *
import sys
import glob
import serial
import time
RightLeftCounter = 90
 
class App:
  def __init__(self, master, ser):
 
    self.ser  = ser
    self.button = Button(master, 
                         text="QUIT", fg="red",
                         command=quit)
    self.button.grid(row=0, column=0, padx=0, pady=0, sticky="nw")
 
    self.slogan = Button(master,
                         text="Reset",
                         command=self.write_reset)
    self.slogan.grid(row=0, column=4, padx=0, pady=0, sticky="nw")
 
    self.Left = Button(master,
                         text="←",padx=10,
                         command=self.write_Left)
    self.Left.grid(row=0, column=1, padx=0, pady=0, sticky="nw")
 
    self.Right = Button(master,
                         text="→",padx=10,
                         command=self.write_Right)
    self.Right.grid(row=0, column=6, padx=2, pady=0, sticky="nw")
    self.sweep = Button(master,
                         text="Sweep",
                         command=self.write_sweep)
    self.sweep.grid(row=0, column=8, padx=0, pady=0, sticky="nw")
 
 
  def write_Left(self):
    global RightLeftCounter
    if (RightLeftCounter>0):
      RightLeftCounter -=1
    self.ser.write(bytes([RightLeftCounter]))
    print(RightLeftCounter)
    print(self.ser.readline())
 
  def write_Right(self):
    global RightLeftCounter
    if (RightLeftCounter<180):
      RightLeftCounter +=1
    self.ser.write(bytes([RightLeftCounter]))
    print(RightLeftCounter)
    print(self.ser.readline())
  def write_reset(self):
    global RightLeftCounter
    RightLeftCounter = 90
    print(RightLeftCounter)
    self.ser.write(bytes([RightLeftCounter]))
    print(self.ser.readline())
 
  def write_sweep(self):
    global RightLeftCounter
    for RightLeftCounter in range(0,180):
      print(RightLeftCounter)
      self.ser.write(bytes([RightLeftCounter]))
      print(self.ser.readline())
      time.sleep(0.01) # delays for 1 seconds
    RightLeftCounter = 90
    self.ser.write(bytes([RightLeftCounter]))
 
def main():
  ser = serial.Serial()
  ser.port = 'COM8'
  ser.baudrate = 9600
  ser.timeout = 0
  # open port if not already open
  if ser.isOpen() == False:
    ser.open()
  root = Tk()
  root.title("ThereminAI")
  root.geometry("300x50+500+300")
  app = App(root,ser)
  root.mainloop()
 
if __name__ == '__main__':
  main()