
# Intercepts serial data from ADC and displays as a voltage across the LDR
# To be used for acquiring voltage measurements with known intensity, for calibration
# Serial data is sent from ADC via I2C to Arduino and then intercepted through the serial monitor

# Imports
import serial
from tkinter import *


# Serial port parameters
serial_speed = 9600
serial_port = 'COM5'

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
            
            #print(floatdata) if testing, output float data to console
            self.temp_data.set(floatdata)
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


