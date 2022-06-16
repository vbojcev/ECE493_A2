import random
from random import randint

import math
from math import sqrt

import matplotlib.pyplot as plt
import numpy as np

plt.style.use('_mpl-gallery')

from matplotlib.pyplot import figure

#figure(figsize=(8, 6), dpi=80)

#enumeration for sensor type -> radius
sensorType = {"A": [100, 300], "B": [70, 170], "C": [30, 65]}

class Target:
    def __init__(self):
        self.location = [random.randint(0,500), random.randint(0,500)] 
        self.k = 0

targets = []

class Sensor:
    def __init__(self, location, type):
        self.location = location
        self.type = type
        self.range = sensorType[type][0]
        self.cost = sensorType[type][1]

    def setType(self, type):
        self.range = sensorType[type][0]
        self.cost = sensorType[type][1]

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

initialLocations = []

globalK = 3

#initialize set of all 500x500 potential sites
for i in range(500):
    for j in range (500):
        initialLocations.append([i, j])

#do not allow sensor and target at the same site
for target in targets:
    if target.location in initialLocations:
        initialLocations.remove(target.location)

sensors = []

numRemoved = 0

print(initialLocations)

for loc in initialLocations:
    sensors.append(Sensor(loc, 'A'))

#compute initial coverage for each target
for sensor in sensors:
    for target in targets:
        if sqrt(pow(sensor.location[0] - target.location[0], 2) + pow(sensor.location[0] - target.location[0], 2)) <= sensor.range:
            target.k += 1

#see which sensors we can remove
for sensor in sensors:
    for target in targets:
        if sqrt(pow(sensor.location[0] - target.location[0], 2) + pow(sensor.location[0] - target.location[0], 2)) <= sensor.range:
            if target.k > globalK:
                target.k -= 1
                sensors.remove(sensor)
                numRemoved += 1

print("Removed in first sweep: ", numRemoved)
numRemoved = 0

#check if we can turn any sensors into type B
for sensor in sensors:
    for target in targets:
        if sqrt(pow(sensor.location[0] - target.location[0], 2) + pow(sensor.location[0] - target.location[0], 2)) <= sensorType["B"][0]:
            if target.k > globalK:
                target.k -= 1
                sensors.setType("B")
                numRemoved += 1

print("Changed to type B: ", numRemoved)
numRemoved = 0

#check if we can turn any sensors into type C
for sensor in sensors:
    for target in targets:
        if sqrt(pow(sensor.location[0] - target.location[0], 2) + pow(sensor.location[0] - target.location[0], 2)) <= sensorType["C"][0]:
            if target.k > globalK:
                target.k -= 1
                sensors.setType("C")
                numRemoved += 1

print("Changed to type B: ", numRemoved)
numRemoved = 0