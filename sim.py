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

#TODO#

#MAKE PURGESENSORS() RUN IN A LOOP UNTIL IT DOESN'T PURGE ANY SENSORS IN A GIEVN LOOP

#FOR A SENSOR THAT ONLY COVERS 1 TARGET, MOVE IT RIGHT UP TO THE TARGET AND DOWNSIZE IT
#ALSO, FOR SENSORS THAT COVER "N" TARGETS BUT N-1 ARE COVERED BY OTHER SENSORS, DO THE SAME FOR THE 1 REMAINING SENSOR
#MAKE COST CALCULATING FUNCTION


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

    def resetK(self, o_SensorManager):
        for target in self.a_Targets:
            target.a_CoveredSensors = []
            target.k=0
            for sensor in o_SensorManager.a_Sensors:
                if target.checkCoverage(sensor) == True:
                    target.k += 1
                    target.a_CoveredSensors.append(sensor)

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
        print("removed Sensors:")
        for sensor in self.a_Sensors:
            if sensor not in a_UpdatedSensorList:
                print(sensor.location)
        self.a_Sensors = a_UpdatedSensorList

    def updateCoverage(self, o_TargetManager):
        for sensor in self.a_Sensors:
            sensor.a_CoveredTargets = []
            for target in o_TargetManager.a_Targets:
                if target.checkCoverage(sensor) == True:
                    sensor.a_CoveredTargets.append(target)

    """def purgeSensors(self):
        a_UpdatedSensorList = []
        i_returner = len(self.a_Sensors)
        for o_Sensor in self.a_Sensors:
            b_Essential = False
            for o_Target in o_Sensor.a_CoveredTargets:
                if o_Target.k - 1 < GLOBAL_K:
                    b_Essential = True
            if (o_Sensor not in a_UpdatedSensorList) and b_Essential:
                a_UpdatedSensorList.append(o_Sensor)
        for sensor in self.a_Sensors:
            if sensor not in a_UpdatedSensorList:
                print ("Removing Sensor at ",sensor.location)
                for target in sensor.a_CoveredTargets:
                    target.k -= 1
        self.a_Sensors = a_UpdatedSensorList
        return i_returner - len(self.a_Sensors)"""
        

    def bringCloser(self):
        returner = 0
        for o_Sensor in self.a_Sensors:
            if len(o_Sensor.a_CoveredTargets) == 1:
                o_Sensor.location[0] = o_Sensor.a_CoveredTargets[0].getXCoordinate() + 1
                o_Sensor.location[1] = o_Sensor.a_CoveredTargets[0].getYCoordinate()
                returner += 1
        return returner

    def reduceSensorsB(self):
        for o_Sensor in self.a_Sensors:
            o_Sensor.setType("B")
            b_Essential = False
            for o_Target in o_Sensor.a_CoveredTargets:
                if o_Target.checkCoverage(o_Sensor) == False:
                    o_Sensor.setType("A")
                    break

    def reduceSensorsC(self):
        for o_Sensor in self.a_Sensors:
            o_Sensor.setType("C")
            b_Essential = False
            for o_Target in o_Sensor.a_CoveredTargets:
                if o_Target.checkCoverage(o_Sensor) == False:
                    o_Sensor.setType("B")
                    break


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


def showStatus():
    for target in o_TargetManager.a_Targets:
        print (target.location," Covered by ",target.k," Sensors: ")
        for sensor in target.a_CoveredSensors:
            print("\t",sensor.location)

    print("\n\n")

    for sensor in o_SensorManager.a_Sensors:
        print (sensor.location," Covers ",len(sensor.a_CoveredTargets)," Targets: ")
        for target in sensor.a_CoveredTargets:
            print("\t",target.location," (K=",target.k,")")

def plot():
    # Now we should plot targets and their covering sensors
    # Configure plot 
    plt.style.use('_mpl-gallery')
    fig = plt.figure()
    ax               = fig.add_subplot(111)
    a_TargetData     = np.array(o_TargetManager.a_Plots)
    a_TargetX, a_TargetY = a_TargetData.T

    ax.scatter(a_TargetX, a_TargetY, s=10, c='b', marker="s", label=f'Targets [{len(o_TargetManager.a_Targets)}]')

    a_Plot_A = []
    a_Plot_B = []
    a_Plot_C = []
    for o_Sensor in o_SensorManager.a_Sensors:
        if o_Sensor.type == "A":
            a_Plot_A.append(o_Sensor.location)
        elif o_Sensor.type == "B":
            a_Plot_B.append(o_Sensor.location)
        elif o_Sensor.type == "C":
            a_Plot_C.append(o_Sensor.location)


    a_SensorData_A          = np.array(a_Plot_A)
    if len(a_Plot_A) > 0:
        a_SensorX_A, a_SensorY_A    = a_SensorData_A.T
        ax.scatter(a_SensorX_A, a_SensorY_A, s=10, c='r', marker="o", label=f'Type A Sensors [{len(a_Plot_A)}]')

    a_SensorData_B          = np.array(a_Plot_B)
    if len(a_Plot_B) > 0:
        a_SensorX_B, a_SensorY_B    = a_SensorData_B.T
        ax.scatter(a_SensorX_B, a_SensorY_B, s=10, c='g', marker="o", label=f'Type B Sensors [{len(a_Plot_B)}]')

    a_SensorData_C          = np.array(a_Plot_C)
    if len(a_Plot_C) > 0:
        a_SensorX_C, a_SensorY_C    = a_SensorData_C.T
        ax.scatter(a_SensorX_C, a_SensorY_C, s=10, c='m', marker="o", label=f'Type C Sensors [{len(a_Plot_C)}]')


    fig.set_size_inches(5, 5)
    plt.legend(loc='upper left');
    ax.set(xlim=(0, X_LIM), ylim=(0, Y_LIM))
    print("[PLOTTING...]")
    plt.show()



def purgeSensors(o_TargetManager, o_SensorManager):
    a_UpdatedSensorList = []
    i_returner = len(o_SensorManager.a_Sensors)
    for o_Sensor in o_SensorManager.a_Sensors:
        b_Essential = False
        for o_Target in o_Sensor.a_CoveredTargets:
            if o_Target.k - 1 < GLOBAL_K:
                b_Essential = True
        ##IF NOT ADDING TO UPDATED SENSOR LIST, MUST UPDATE THE K OF ALL ITS TARGETS!!!
        if (o_Sensor not in a_UpdatedSensorList) and b_Essential:
            a_UpdatedSensorList.append(o_Sensor)
        elif b_Essential == False:
            for o_Target in o_Sensor.a_CoveredTargets:
                o_Target.k -= 1
    for sensor in o_SensorManager.a_Sensors:
        if sensor not in a_UpdatedSensorList:
            print ("Removing Sensor at ",sensor.location)
    o_SensorManager.a_Sensors = a_UpdatedSensorList
    return i_returner - len(o_SensorManager.a_Sensors)


def calculateCost(o_SensorManager):
    sum = 0
    for sensor in o_SensorManager.a_Sensors:
        sum += sensor.cost
    return sum

# Main Call ------------------------------------------------------
if __name__ == '__main__':
    print('Running sim\n\n\n')

    # Create Targets, managed by a TargetManager
    i_NumTargets        = 17 
    o_TargetManager     = createTargetNodes(i_NumTargets)

    o_SensorManager = createSensorNodes(o_TargetManager)
    o_TargetManager.resetK(o_SensorManager)
    o_SensorManager.updateCoverage(o_TargetManager)

    print("-------------------------------------------------------------")
    print(f"Number of initial sensors: {len(o_SensorManager.a_Sensors)}")
    showStatus()
    print("-------------------------------------------------------------")
    plot()

    o_SensorManager.updateSensors(o_TargetManager)
    o_TargetManager.resetK(o_SensorManager)
    o_SensorManager.updateCoverage(o_TargetManager)

    print('\n\n\n')
    print("-------------------------------------------------------------")
    print(f"Number of updated sensors: {len(o_SensorManager.a_Sensors)}")
    showStatus()
    print("-------------------------------------------------------------")
    plot()

    purgeSensors(o_TargetManager, o_SensorManager)
    o_TargetManager.resetK(o_SensorManager)
    o_SensorManager.updateCoverage(o_TargetManager)

    print('\n\n\n')
    print("-------------------------------------------------------------")
    print(f"Number of purged sensors: {len(o_SensorManager.a_Sensors)}")
    showStatus()
    print("-------------------------------------------------------------")
    plot()

    movedSensors = o_SensorManager.bringCloser()
    o_TargetManager.resetK(o_SensorManager)
    o_SensorManager.updateCoverage(o_TargetManager)

    print('\n\n\n')
    print("-------------------------------------------------------------")
    print(f"Number of moved sensors: ",movedSensors)
    showStatus()
    print("-------------------------------------------------------------")
    plot()

    o_SensorManager.reduceSensorsB()
    o_TargetManager.resetK(o_SensorManager)
    o_SensorManager.updateCoverage(o_TargetManager)

    print('\n\n\n')
    print("-------------------------------------------------------------")
    print("Changing to type B if possible...")
    showStatus()
    print("-------------------------------------------------------------")
    plot()

    o_SensorManager.reduceSensorsC()
    o_TargetManager.resetK(o_SensorManager)
    o_SensorManager.updateCoverage(o_TargetManager)

    print('\n\n\n')
    print("-------------------------------------------------------------")
    print("Changing to type C if possible...")
    showStatus()
    print("-------------------------------------------------------------")
    plot()

    print("TOTAL COST: ",calculateCost(o_SensorManager))    