import numpy as np
import math
import matplotlib.pyplot as plt
import random

seedX = [0]
seedY = [0]
distances = [0]

# Generate random points
def generate_random(num=20):
  for _ in range(num-1):
    r = random.uniform(2.5, 15)
    theta = math.radians(random.uniform(0, 360))
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    seedX.append(round(x, 2))
    seedY.append(round(y, 2))
generate_random()

def calculate_distance(x1, y1, x2, y2):
  return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# Calculate distances
for i in range(1, len(seedX)):
  distances.append(round(calculate_distance(0, 0, seedX[i], seedY[i]), 2))

# Pretty print results
print("seedX\tseedY\tdistances")
for x, y, d in zip(seedX, seedY, distances):
  print(f"{x}\t{y}\t{d}")

# Show plot
plt.plot(0, 0, 'rx')
plt.plot(seedX[1:], seedY[1:], "*")
plt.show()
