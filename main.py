import numpy as np
import math
import matplotlib.pyplot as plt
import random

seedX = [0]
seedY = [0]
distances = [0]
closest_seeds_index = []

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

# Set graph axes
plt.xlim(-15, 15)
plt.ylim(-15, 15)

def find_closest(): # Identify the closest point to the origin
  distances_copy = distances.copy()
  
  closest_index = distances_copy.index(min(distances_copy[1:]))
  while closest_index in closest_seeds_index:
    distances_copy[closest_index] = 100
    closest_index = distances_copy.index(min(distances_copy[1:]))

  closest_x = seedX[closest_index]
  closest_y = seedY[closest_index]
  closest_seeds_index.append(closest_index)
  return closest_x, closest_y

for _ in range(3):
  closest_x, closest_y = find_closest()
  
  # Draw a line from origin to the closest point
  plt.plot([0, closest_x], [0, closest_y], 'r--')

  # Find the unit vector
  magnitude = math.sqrt(closest_x**2 + closest_y**2)
  unit_vector_x = -1*(closest_x / magnitude) # Reverse the direction so that it points to origin
  unit_vector_y = -1*(closest_y / magnitude)
  plt.arrow(closest_x, closest_y, unit_vector_x, unit_vector_y, head_width=0.3, head_length=0.5, fc='b', ec='b')

  # Draw a line perpendicular to the unit vector
  perpendicular_x = -unit_vector_y
  perpendicular_y = unit_vector_x
  x_values = [-15, 15] # Seemingly infinite line (ray)
  y_values = [closest_y + perpendicular_y * (x - closest_x) / perpendicular_x for x in x_values]
  plt.plot(x_values, y_values, 'g--')

# Show plot
plt.plot(0, 0, 'x', markersize=10, color='purple')
plt.plot(seedX[1:], seedY[1:], "*", markersize=5)
plt.show()
