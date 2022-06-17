# File Information ---------------------------------------------
# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
# 	File Name: sim.py
#
# 	File Description: 
# 
# 	File History:
#       - 2022-06-15: Created by Vojdan B.
# 		- 2022-06-17: Debugged by Rohit S.
# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 

# Imports --------------------------------------------------------
from random import randint
from math import sqrt
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import figure

# Global Variables -----------------------------------------------

# Class Declarations ---------------------------------------------
# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
#	Class Name: Target
#
#	Class Description: 
# 
#	Class History: 
#       - 2022-06-15: Created by Vojdan B.
# 
# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
class Target:
    def __init__(self, i_ID):
        self.i_ID       = i_ID
        self.location   = [randint(0,500), randint(0,500)] 
        self.k          = 0

    def getXCoordinate(self):
        return self.location[0]

    def getYCoordinate(self):
        return self.location[1]

    def printCoordinates(self):
        print(f"X = {self.getXCoordinate()}, Y = {self.getYCoordinate()}")

    def checkCoverage(self, sensor):
        return sqrt(pow(sensor.location[0] - self.location[0], 2) + pow(sensor.location[1] - self.location[1], 2)) <= sensor.range
    

# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
#	Class Name: Target
#
#	Class Description: 
# 
#	Class History: 
#       - 2022-06-15: Created by Vojdan B.
# 
# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
class Sensor:
    def __init__(self, location, type):
        self.location = location
        self.type = type
        self.setType(self.type)

    def setType(self, type):
        self.range = sensorType[type][0]
        self.cost = sensorType[type][1]

    def __str__(self):
        return f"Type {self.type} sensor at {self.location[0]},{self.location[1]}"

# Function Declarations ------------------------------------------

# Main Call ------------------------------------------------------
if __name__ == '__main__':
    print('Running sim')

    # Configure plot 
    plt.style.use('_mpl-gallery')

    #enumeration for sensor type -> radius
    sensorType = {"A": [100, 300], "B": [70, 170], "C": [30, 65]}

    # Create an empty array to store created targets
    targets = []

    # Create i nodes and store in targets
    for i in range(17):
        targets.append(Target(i_ID=i))

    # Show location of each node, store in occupied array
    a_Occupied = []
    for node in targets:
        node.printCoordinates()
        a_Occupied.append(node.location)

    print(a_Occupied)

    # Create an empty array to store plots
    plotArr = []

    # Go through each node and store location data in plot array
    for node in targets:
        plotArr.append(node.location)

    # Create plot
    fig, ax = plt.subplots()

    # Convert location data to np array for plotting
    data = np.array(plotArr)

    # Get x and y coordinates from data
    x, y = data.T

    # Create scatter plot
    ax.scatter(x, y)

    # Configure and show plot
    fig.set_size_inches(5, 5)
    ax.set(xlim=(0, 500), ylim=(0, 500))
    plt.show()

    # Create array to store potential sites
    initialLocations = []

    globalK = 3

    #initialize set of all 500x500 potential sites
    for i in range(500):
        for j in range (500):
            if [i, j] in a_Occupied:
                # If a target is there, don't save it as a potential type
                pass 
            else:
                # If nothing is there, it is an initial location
                initialLocations.append([i, j])

    # Create variables to store sensor info
    sensors = []
    numRemoved = 0
    toRemove = []

    a_GoodSensors = []      

    # For every location, add a sensor to it
    for loc in initialLocations:
        # Create a sensor object at specific location
        o_Sensor = Sensor(loc, 'A')
        # Attach to sensors array
        sensors.append(o_Sensor)
        # Compute initial coverage for each target
        for target in targets:
            inRange = target.checkCoverage(o_Sensor)
            if inRange:
                target.k += 1
                if target.k > globalK:
                    target.k -= 1
                    numRemoved += 1
                else:
                    a_GoodSensors.append(o_Sensor)

    print("Removed in first sweep: ", numRemoved)
    numRemoved = 0

    sensors = a_GoodSensors

    #check if we can turn any sensors into type B
    for sensor in sensors:
        for target in targets:
            if sqrt(pow(sensor.location[0] - target.location[0], 2) + pow(sensor.location[1] - target.location[1], 2)) <= sensorType["B"][0]:
                if target.k > globalK:
                    target.k -= 1
                    sensor.setType("B")
                    numRemoved += 1

    print("Changed to type B: ", numRemoved)
    numRemoved = 0

    #check if we can turn any sensors into type C
    for sensor in sensors:
        for target in targets:
            if sqrt(pow(sensor.location[0] - target.location[0], 2) + pow(sensor.location[1] - target.location[1], 2)) <= sensorType["C"][0]:
                if target.k > globalK:
                    target.k -= 1
                    sensor.setType("C")
                    numRemoved += 1

    print("Changed to type B: ", numRemoved)
    numRemoved = 0

    print(sensors)

    plotArr = []

    for sensor in sensors:
        plotArr.append(sensor.location)

    fig, ax = plt.subplots()

    data = np.array(plotArr)

    x, y = data.T

    ax.scatter(x, y)

    fig.set_size_inches(5, 5)

    ax.set(xlim=(0, 500), ylim=(0, 500))

    plt.show()