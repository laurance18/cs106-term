import numpy as np
import math
import matplotlib.pyplot as plt
import random

# SECTION: Global variables
perm_seedX = [0]
perm_seedY = [0]
current_seedX = []
current_seedY = []
distances = []

removed_seeds = []
previous_seeds = []

# SECTION: Random point generation
def generate_random(num=20):
  global current_seedX, current_seedY, perm_seedX, perm_seedY
  
  for _ in range(num-1):
    r = random.uniform(2.5, 15)
    theta = math.radians(random.choice([x for x in range(361) if x not in [0, 90, 180, 360]]))
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    perm_seedX.append(round(x, 2))
    perm_seedY.append(round(y, 2))
  current_seedX = perm_seedX.copy()
  current_seedY = perm_seedY.copy()
generate_random()

# SECTION: Distance calculation
for x, y in zip(perm_seedX, perm_seedY):
  distances.append(round(math.sqrt(x**2 + y**2), 2))

# SECTION: Pretty printing results
print("seedX\tseedY\tdistances")
for x, y, d in zip(perm_seedX, perm_seedY, distances):
  print(f"{x}\t{y}\t{d}")

# SECTION: Fi the closest seeds to the origin
def find_closest():
  global previous_seeds
  distance_wo_origin = distances[1:]

  closest_index = distance_wo_origin.index(min(distance_wo_origin))
  while perm_seedX[closest_index+1] in previous_seeds:
    distance_wo_origin[closest_index] = math.inf
    closest_index = distance_wo_origin.index(min(distance_wo_origin))
  closest_x = perm_seedX[closest_index+1]
  closest_y = perm_seedY[closest_index+1]

  previous_seeds.append(perm_seedX[closest_index+1])
  return closest_x, closest_y

for _ in range(2):
  closest_x, closest_y = find_closest()
  print(f"Closest seed {len(previous_seeds)}: {closest_x}, {closest_y}")

  # SECTION: Draw line from closest point to the origin
  plt.plot([0, closest_x], [0, closest_y], '--', color="purple")

  # SECTION: Calculate and draw unit vector
  magnitude = math.sqrt(closest_x**2 + closest_y**2)
  unit_vector_x = -1*(closest_x / magnitude) # Multiply by -1 to flip the unit vector
  unit_vector_y = -1*(closest_y / magnitude)
  plt.arrow(closest_x, closest_y, unit_vector_x, unit_vector_y, head_width=0.3, head_length=0.3, fc='red', ec='red')

  # SECTION: Draw a line perpendicular to the unit vector
  perpendicular_x = -unit_vector_y
  perpendicular_y = unit_vector_x
  x_values = [-15, 15] # Seemingly infinite line (ray)
  y_values = [closest_y + perpendicular_y * (x - closest_x) / perpendicular_x for x in x_values]
  plt.plot(x_values, y_values, 'g--')

  # SECTION: Draw unit vectors from closest to other seeds
  for i in range(1, len(perm_seedX)):
    if perm_seedX[i] == closest_x and perm_seedY[i] == closest_y:
      continue
    dx = perm_seedX[i] - closest_x
    dy = perm_seedY[i] - closest_y
    magnitude = math.sqrt(dx**2 + dy**2)
    unit_x_from = dx / magnitude
    unit_y_from = dy / magnitude

    # SECTION: Calculate dot product and remove accordingly
    dot_product = unit_x_from * unit_vector_x + unit_y_from * unit_vector_y
    if dot_product < 0:
      plt.arrow(perm_seedX[i], perm_seedY[i], unit_x_from, unit_y_from, head_width=0.3, head_length=0.3, fc='red', ec='red')
    else:
      plt.arrow(perm_seedX[i], perm_seedY[i], unit_x_from, unit_y_from, head_width=0.3, head_length=0.3, fc='blue', ec='blue')

# Set graph axes
plt.xlim(-15, 15)
plt.ylim(-15, 15)

plt.plot(0, 0, 'x', markersize=10, color='orange')
plt.plot(current_seedX[1:], current_seedY[1:], ".b", markersize=5)
plt.show()