import numpy as np
import math
import matplotlib.pyplot as plt
import random

perm_seedX = [0]
perm_seedY = [0]

# SECTION: Random point generation
def generate_random(num=20):
  for _ in range(num-1):
    r = random.uniform(2.5, 15)
    theta = math.radians(random.choice([x for x in range(361) if x not in [0, 90, 180, 360]]))
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    perm_seedX.append(round(x, 2))
    perm_seedY.append(round(y, 2))
generate_random(20)

plt.plot(0, 0, 'x', markersize=10, color='orange')
plt.plot(perm_seedX[1:], perm_seedY[1:], ".b", markersize=5)
plt.show()