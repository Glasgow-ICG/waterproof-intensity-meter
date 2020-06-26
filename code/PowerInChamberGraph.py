#plot data acquired from LDRPowerFromVoltage script to demonstrate lower intensities measured while submerged

#imports
import csv
import matplotlib.pyplot as plt
import numpy as np

plt.style.use('seaborn-paper')

def read_dataset(filename):
    x = []
    y = []

    with open(filename, "r") as csvfile:
        plots = csv.reader(csvfile, delimiter="\t")
        for row in plots:
            x.append(float(row[0]))
            y.append(float(row[1]))

    # cast to native numpy arrays
    x = np.array(x)
    y = np.array(y)
    z = np.log(x)
    return (x, y, z)

#read in datasets acquired using LDRPowerFromVoltage script when sensor is dry or submerged
#note that in order to compare these datasets, transmittance was omitted from power calculation
tldry, powerdry, logdry = read_dataset("561nmdrychamberpower.txt")
tlwet, powerwet, logwet = read_dataset("561nmwetchamberpower.txt")

plt.scatter(tldry, powerdry, label = "In air")
plt.scatter(tlwet, powerwet, label = "In water")

v = np.linspace(0,2500,50) #generate line to plot

plt.plot(v,v, label = "Expected power in dry chamber", color = "black",linestyle = "dashed", linewidth = 0.5)
plt.title("Laser power measurements in dry and submerged sample chamber")
plt.ylabel("Power measured in chamber (microW)")
plt.xlabel("Power measured at back focus of objective (microW)")
plt.legend()
plt.show
