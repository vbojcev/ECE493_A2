# File Information ---------------------------------------------
# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
# 	File Name: sim.py
#
# 	File Description: 
# 
# 	File History:
#       - 2022-06-15: Created by Vojdan B.
# 		- 2022-06-17: Debugged by by Rohit S.
# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 

# Imports --------------------------------------------------------
from random import randint
from math import sqrt
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import numpy as np

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
    def __init__(self):
        self.location = [randint(0,500), randint(0,500)] 
        self.k=0

    def covInc():
        k+=1

    def covDec():
        k-=1

# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
#	Class Name: Sensor
#
#	Class Description: 
# 
#	Class History: 
#       - 2022-06-15: Created by Vojdan B.
# 
# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
class Sensor:
    def __init__(self, location, type):
        self.location=location
        self.type=type
        self.range=sensorType[type][0]
        self.cost=sensorType[type][1]

# Function Declarations ------------------------------------------
# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
#
#	Function Name: checkCoverage
#
#	Function Description:
#
#	Function Inputs:
#       - target:
#       - sensor:
#
#	Function Outputs:
#
#	Function History:
#		- 2022-06-17: Created by Rohit S.
#
# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
def checkCoverage(target, sensor):
    if (sqrt(pow() + pow()) <= sensor.range):
        target.covInc()
    else:
        target.covDec()

# Main Call ------------------------------------------------------
if __name__ == '__main__':
    print('Running sim')
    plt.style.use('_mpl-gallery')
    sensorType = {"A": [100, 300], "B": [70, 170], "C": [30, 65]}
    targets = []
    for i in range(17):
        targets.append(Target())

    for node in targets:
        print(node.location[0], ", ", node.location[1])

    plotArr = []

    for node in targets:
        plotArr.append(node.location)

    fig, ax = plt.subplots()

    data = np.array(plotArr)

    x, y = data.T

    ax.scatter(x, y)

    fig.set_size_inches(5, 5)

    ax.set(xlim=(0, 500), ylim=(0, 500))

    plt.show()
#figure(figsize=(8, 6), dpi=80)




        


