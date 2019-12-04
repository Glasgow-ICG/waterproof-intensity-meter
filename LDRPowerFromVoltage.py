
# Read in serial data, assign power value corresponding to fitted polynomial from calibration text file, display power in Tkinter GUI

# Imports
import serial
from tkinter import *

import csv
import numpy as np
from numpy.polynomial import Polynomial


transmittance = 0.6725 #transmittance of system between point where known power readings were taken and sensor
deg = 5 #polynomial fitting degree - be careful! too high a degree will overfit a polynomial and mis-estimate power

# Serial port parameters
serial_speed = 9600
serial_port = 'COM5'


def read_dataset(filename):
    x = []
    y = []

    with open(filename, "r") as csvfile:
        plots = csv.reader(csvfile, delimiter="\t")
        for row in plots:
            x.append(float(row[0]))
            y.append(float(row[1]))

    # cast to native numpy arrays, and give log(x)
    x = np.array(x) * transmittance #apply transmittance to power meter readings
    y = np.array(y)
    z = np.log(x)
    
    print (y)
    return (x, y, z)


thorlabs561, ldr561, log561 = read_dataset("3ldr561nmchambertransmittance.txt") #read in previous calibration data
p, resid = Polynomial.fit(ldr561, log561, deg, full = True) #fit log-log polynomial
ser = serial.Serial(serial_port, serial_speed, timeout=1) #open serial port

# Main Tkinter application
class Application(Frame):

    # Measure data from the sensor
    def measure(self):

        # Request data and read the answer
        data = ser.readline()
        

        # If the answer is not empty and not text, process & display data
        if (data != ""):
            newdata = data.decode('utf-8')
            try:
                floatdata = float(newdata)
            except (ValueError, IndexError):
                floatdata = 0  #skip non-integer serial results (eg. ADC initialisation)
            powerdata = round(np.exp(p(floatdata)), 2) #convert to power via polynomial
            
            #print(floatdata) if testing, output float data to console
            self.temp_data.set(powerdata)
            self.lux.pack()

        # Wait 10 milliseconds between each measurement
        self.after(10,self.measure)

    # Create display elements
    def createWidgets(self):

        self.lux = Label(self, textvariable=self.temp_data, font=('Tahoma', 40, 'bold'))
        self.temp_data.set("")
        self.lux.pack()

    
    # Initialise variables and begin measurements
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.temp_data = StringVar()
        self.createWidgets()
        self.pack()
        self.measure()

# Create and run the GUI
root = Tk()
app = Application(master=root)
app.mainloop()


