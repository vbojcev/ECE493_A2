import random
from random import randint

class Target:
    def __init__(self):
        self.x = random.randint(0,500)
        self.y = random.randint(0,500)

targets = []

for i in range(17):
    targets.append(Target())

for node in targets:
    print(node.x, ", ", node.y);