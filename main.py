import numpy as np
import math
import matplotlib.pyplot as plt
import random

seedX = [0]
seedY = [0]
final_seedX = [0]
final_seedY = [0]
distances = [0]
closest_seeds_index = []

# SECTION: Random point generation
def generate_random(num=20):
  for _ in range(num-1):
    r = random.uniform(2.5, 15)
    theta = math.radians(random.uniform(5, 360))
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    seedX.append(round(x, 2))
    seedY.append(round(y, 2))
generate_random()

# SECTION: Distance calculation
def calculate_distance(x1, y1, x2, y2):
  return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

for i in range(1, len(seedX)):
  distances.append(round(calculate_distance(0, 0, seedX[i], seedY[i]), 2))

# Pretty print results
print("seedX\tseedY\tdistances")
for x, y, d in zip(seedX, seedY, distances):
  print(f"{x}\t{y}\t{d}")

# Set graph axes
plt.xlim(-15, 15)
plt.ylim(-15, 15)

# SECTION: Find the closest point to the origin
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

# SECTION: Main Loop
for _ in range(2):
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

  # SECTION: Draw unit vectors from closest to other seeds
  seed_remove_index = []
  for i in range(1, len(seedX)):
    if i not in closest_seeds_index:
      dx = seedX[i] - closest_x
      dy = seedY[i] - closest_y
      magnitude = math.sqrt(dx**2 + dy**2)
      unit_x_to = (dx / magnitude)
      unit_y_to = (dy / magnitude)

      dot_product = unit_x_to * unit_vector_x + unit_y_to * unit_vector_y
      if dot_product >= 0:
        print(f"Seed {i} is on the same side as the origin")
      else:
        print(f"Seed {i} is on the opposite side as the origin")
        seed_remove_index.append(i)
  for k in range(1, len(seedX)): # Remove seeds at opposite side of the origin
    if k in seed_remove_index:
      continue
    else:
      final_seedX.append(seedX[k])
      final_seedY.append(seedY[k])

  seedX = final_seedX.copy() # Reset the lists
  seedY = final_seedY.copy()
  final_seedX = []
  final_seedY = []

# Show final plot
plt.plot(0, 0, 'x', markersize=10, color='purple')
plt.plot(seedX[1:], seedY[1:], "*", markersize=5)
plt.show()
