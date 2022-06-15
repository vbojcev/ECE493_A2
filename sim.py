import random
from random import randint

import math
from math import sqrt

sensorClass = {"A": [100, 300], "B": [70, 170], "C": [30, 65]}

class Target:
    def __init__(self):
        self.location = [random.randint(0,500), random.randint(0,500)] 
        self.k=0

    def covInc():
        k+=1

    def covDec():
        k-=1

targets = []

class Sensor:
    def __init__(self, location, type):
        self.location=location
        self.type=type
        self.range=sensorClass[type][0]
        self.cost=sensorClass[type][1]
        
def checkCoverage(target, sensor):
    if (sqrt(pow() + pow()) <= sensor.range):
        target.covInc()
    else:
        target.covDec()

for i in range(17):
    targets.append(Target())

for node in targets:
    print(node.location[0], ", ", node.location[1])