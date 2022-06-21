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

# Global Variables -----------------------------------------------
X_LIM = 500
Y_LIM = 500

SENSOR_TYPE = {"A": [100, 300], "B": [70, 170], "C": [30, 65]}
GLOBAL_K = 1


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
        self.location           = [randint(0,X_LIM), randint(0,Y_LIM)] 
        self.a_CoveredSensors   = [] 
        self.k                  = 0

    def getXCoordinate(self):
        return self.location[0]

    def getYCoordinate(self):
        return self.location[1]

    def printCoordinates(self):
        print(f"X = {self.getXCoordinate()}, Y = {self.getYCoordinate()}")

    def checkCoverage(self, sensor):
        b_IsCovered = sqrt(pow(sensor.location[0] - self.location[0], 2) + pow(sensor.location[1] - self.location[1], 2)) <= sensor.range
        return b_IsCovered
# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
#	Class Name: TargetManager
#
#	Class Description:  Manages Target instances
# 
#	Class History: 
#       - 2020-06-17: Created by Rohit S.
# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .     
class TargetManager:
    def __init__(self):
        self.a_Targets          = []
        self.a_Occupied         = []
        self.a_Plots            = []
        self.d_Coverage         = {}

    def addTarget(self, o_Target):
        self.a_Targets.append(o_Target)
        self.a_Occupied.append(o_Target.location)
        self.a_Plots.append(o_Target.location)

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
        self.location = location
        self.type = type
        self.setType(self.type)
        self.b_isOn = True
        self.a_CoveredTargets = []

    def setType(self, type):
        self.range = SENSOR_TYPE[type][0]
        self.cost = SENSOR_TYPE[type][1]

    def turnOff(self):
        self.b_isOn = False

    def setCoveredTargets(self, o_TargetManager):
        # For this sensor, go through each target
        for o_Target in o_TargetManager.a_Targets:
            # For each target, check if this sensor covers it
            if o_Target.checkCoverage(self):
                # Ensure that we didn't already mark this target as covered
                if self not in o_Target.a_CoveredSensors:
                    self.a_CoveredTargets.append(o_Target)
                    o_Target.k += 1
                    o_Target.a_CoveredSensors.append(self)
                if o_Target.k > GLOBAL_K:
                    i_MinCover = 1000000
                    # We have to remove the least covering node
                    for o_Sensor in o_Target.a_CoveredSensors:
                        if len(o_Sensor.a_CoveredTargets) <= i_MinCover:
                            i_MinCover = len(o_Sensor.a_CoveredTargets)
                            o_BadSensor = o_Sensor
                    o_BadSensor.a_CoveredTargets.remove(o_Target)
                    o_Target.a_CoveredSensors.remove(o_BadSensor)
                    o_Target.k -= 1

    def __str__(self):
        return f"Type {self.type} sensor at {self.location[0]},{self.location[1]}"

# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
#	Class Name: SensorManager
#
#	Class Description: Manages Sensors
# 
#	Class History: 
#       - 2020-06-17: Created by Rohit S. 
#
# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
class SensorManager:
    def __init__(self):
        self.a_Sensors = []

    def addSensor(self, o_Sensor):
        self.a_Sensors.append(o_Sensor)

    def updateSensors(self, o_TargetManager):
        a_UpdatedSensorList = []
        for o_Target in o_TargetManager.a_Targets:
            for o_Sensor in o_Target.a_CoveredSensors:
                if o_Sensor not in a_UpdatedSensorList:
                    a_UpdatedSensorList.append(o_Sensor)

        self.a_Sensors = a_UpdatedSensorList

    def purgeSensors(self):
        a_UpdatedSensorList = []
        for o_Sensor in self.a_Sensors:
            b_Essential = False
            for o_Target in o_Sensor.a_CoveredTargets:
                if o_Target.k - 1 < GLOBAL_K:
                    b_Essential = True
            if (o_Sensor not in a_UpdatedSensorList) and b_Essential:
                a_UpdatedSensorList.append(o_Sensor)
        self.a_Sensors = a_UpdatedSensorList


# Function Declarations ------------------------------------------
# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
#
#	Function Name: createTargetNodes
#
#	Function Description:   Creates n target objects, returned in 
#                           an array
#
#	Function Inputs:
#       - i_NumTargets: Number of targets to be made
#
#	Function Outputs:
#       - o_TargetManager: Object to manage targets
#
#	Function History:
#		- 2022-06-17: Created by Rohit S.
#
# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
def createTargetNodes(i_NumTargets):
    o_TargetManager = TargetManager()
    for _ in range(0, i_NumTargets):
        o_TargetManager.addTarget(Target(i_ID=_))
    return o_TargetManager

# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
#
#	Function Name: createSensorNodes
#
#	Function Description:
#
#	Function Inputs:
#       - o_TargetManager: Used to gain info on TargetLocations
#
#	Function Outputs:
#
#	Function History:
#		- 2022-06-17: Created by Rohit S.
#
# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
def createSensorNodes(o_TargetManager):
    o_SensorManager = SensorManager()
    for x in range(0, X_LIM):
        for y in range(0, Y_LIM):
            # Check if space is free
            if [x, y] not in o_TargetManager.a_Occupied:
                # Create a sensor at unoccupied space
                o_Sensor = Sensor([x,y], "A")
                # For the sensor at that space, check how many targets
                #   are covered
                o_Sensor.setCoveredTargets(o_TargetManager)
                # If the sensor isn't covering any targets, don't use it
                if len(o_Sensor.a_CoveredTargets) != 0:
                    o_SensorManager.addSensor(o_Sensor)


    return o_SensorManager

# Main Call ------------------------------------------------------
if __name__ == '__main__':
    print('Running sim')

    # Create Targets, managed by a TargetManager
    i_NumTargets        = 17 
    o_TargetManager     = createTargetNodes(i_NumTargets)

    o_SensorManager = createSensorNodes(o_TargetManager)

    print(f"Number of sensors: {len(o_SensorManager.a_Sensors)}")

    o_SensorManager.updateSensors(o_TargetManager)

    print(f"Number of sensors: {len(o_SensorManager.a_Sensors)}")

    #updateK()

    o_SensorManager.purgeSensors()

    print(f"Number of sensors: {len(o_SensorManager.a_Sensors)}")

    for target in o_TargetManager.a_Targets:
        print (target.location," ",target.k)

    # Now we should plot targets and their covering sensors
    # Configure plot 
    plt.style.use('_mpl-gallery')
    fig = plt.figure()
    ax               = fig.add_subplot(111)
    a_TargetData     = np.array(o_TargetManager.a_Plots)
    a_TargetX, a_TargetY = a_TargetData.T

    a_Plot = []
    for o_Sensor in o_SensorManager.a_Sensors:
        a_Plot.append(o_Sensor.location)
    a_SensorData            = np.array(a_Plot)
    a_SensorX, a_SensorY    = a_SensorData.T

    ax.scatter(a_TargetX, a_TargetY, s=10, c='b', marker="s", label=f'Targets [{len(o_TargetManager.a_Targets)}]')
    ax.scatter(a_SensorX, a_SensorY, s=10, c='r', marker="o", label=f'Sensors [{len(o_SensorManager.a_Sensors)}]')
    
    fig.set_size_inches(5, 5)
    plt.legend(loc='upper left');
    ax.set(xlim=(0, X_LIM), ylim=(0, Y_LIM))
    plt.show()




    # #check if we can turn any sensors into type B
    # for sensor in sensors:
    #     for target in targets:
    #         if sqrt(pow(sensor.location[0] - target.location[0], 2) + pow(sensor.location[1] - target.location[1], 2)) <= SENSOR_TYPE["B"][0]:
    #             if target.k > GLOBAL_K:
    #                 target.k -= 1
    #                 sensor.setType("B")
    #                 numRemoved += 1

    # print("Changed to type B: ", numRemoved)
    # numRemoved = 0

    # #check if we can turn any sensors into type C
    # for sensor in sensors:
    #     for target in targets:
    #         if sqrt(pow(sensor.location[0] - target.location[0], 2) + pow(sensor.location[1] - target.location[1], 2)) <= SENSOR_TYPE["C"][0]:
    #             if target.k > GLOBAL_K:
    #                 target.k -= 1
    #                 sensor.setType("C")
    #                 numRemoved += 1

    # print("Changed to type B: ", numRemoved)
    # numRemoved = 0

    # print(sensors)

    # plotArr = []

    # for sensor in sensors:
    #     plotArr.append(sensor.location)

    # fig, ax = plt.subplots()

    # data = np.array(plotArr)

    # x, y = data.T

    # ax.scatter(x, y)

    # fig.set_size_inches(5, 5)

    # ax.set(xlim=(0, 500), ylim=(0, 500))

    # plt.show()