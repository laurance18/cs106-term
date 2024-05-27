import numpy as np
import math
import matplotlib.pyplot as plt
import random

seedX = [0]
seedY = [0]

# Generate random points
def generateRandom(num=20):
  for _ in range(num-1):
    r = random.uniform(2.5, 15)
    theta = math.radians(random.uniform(0, 360))
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    seedX.append(round(x, 2))
    seedY.append(round(y, 2))


generateRandom()

# Show plot
plt.scatter(0, 0, color='red')
plt.scatter(seedX[1:], seedY[1:])
plt.show()
