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

removed_seedsX = []
removed_seedsY = []
previous_seeds = []

unit_vector_mp = []
perp_lines_slope = []

# SECTION: Random point generation
def generate_random(num=20):
  global current_seedX, current_seedY, perm_seedX, perm_seedY
  
  for _ in range(num//4):
    r = random.uniform(2.5, 15)
    theta = math.radians(random.choice([x for x in range(5, 85)]))
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    perm_seedX.append(round(x, 2))
    perm_seedY.append(round(y, 2))

  for _ in range(num//4):
    r = random.uniform(2.5, 15)
    theta = math.radians(random.choice([x for x in range(95, 175)]))
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    perm_seedX.append(round(x, 2))
    perm_seedY.append(round(y, 2))

  for _ in range(num//4):
    r = random.uniform(2.5, 15)
    theta = math.radians(random.choice([x for x in range(185, 265)]))
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    perm_seedX.append(round(x, 2))
    perm_seedY.append(round(y, 2))

  for _ in range(num//4):
    r = random.uniform(2.5, 15)
    theta = math.radians(random.choice([x for x in range(275, 355)]))
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

# SECTION: Pretty printing seed coordinates & distances
print("seedX\tseedY\tdistances")
for x, y, d in zip(perm_seedX, perm_seedY, distances):
  print(f"{x}\t{y}\t{d}")

# SECTION: Find the closest seeds to the origin
def find_closest():
  global previous_seeds, distances

  distances_copy = distances[:]
  distances_copy[0] = 100 # Arbitrary large number / Will help us to figure out when to end the loop

  for i in range(1,len(current_seedX)):
    if current_seedX[i] in previous_seeds:
      distances_copy[i] = 100 # Arbitrary large number
    if current_seedX[i] in removed_seedsX:
      distances_copy[i] = 100

  closest_index = distances_copy.index(min(distances_copy))
  closest_x = current_seedX[closest_index]
  closest_y = current_seedY[closest_index]

  previous_seeds.append(perm_seedX[closest_index])
  return closest_x, closest_y

while True: # Will be broken when there are no more seeds to process (closest_x == 0 and closest_y == 0)
  closest_x, closest_y = find_closest()
  if closest_x == 0 and closest_y == 0:
    break
  print(f"Closest seed {len(previous_seeds)}: {closest_x}, {closest_y}")

  # SECTION: Draw line from closest point to the origin
  midpoint_x = (0 + closest_x) / 2 # Record the midpoint of unit vector
  midpoint_y = (0 + closest_y) / 2
  unit_vector_mp.append((midpoint_x, midpoint_y))

  # SECTION: Calculate unit vector
  magnitude = math.sqrt(closest_x**2 + closest_y**2)
  unit_vector_x = -1*(closest_x / magnitude) # Multiply by -1 to flip the unit vector
  unit_vector_y = -1*(closest_y / magnitude)

  # SECTION: Draw a line perpendicular to the unit vector
  perpendicular_x = -unit_vector_y
  perpendicular_y = unit_vector_x
  x_values = np.linspace(-15, 15, 100) # Extend the line to whole graph
  y_values = [closest_y + perpendicular_y * (x - closest_x) / perpendicular_x for x in x_values]
  perp_lines_slope.append(perpendicular_y / perpendicular_x) # Record the slope of the perpendicular line

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
      removed_seedsX.append(perm_seedX[i]) # Add to removed seeds for future reference
      removed_seedsY.append(perm_seedY[i])
    else:
      continue

# SECTION: Find intersection of perpendicular lines

def find_intersection(slope1, intercept1, slope2, intercept2):
    # If the slopes are equal, the lines are parallel and have no intersection
    if slope1 == slope2:
        return None

    x = (intercept2 - intercept1) / (slope1 - slope2)
    y = slope1 * x + intercept1
    return (x, y)

# SECTION: Draw perpendicular lines from the midpoint of unit vectors

intersections = []
for i in range(len(perp_lines_slope)):
    for j in range(i+1, len(perp_lines_slope)):
        slope1 = perp_lines_slope[i]
        intercept1 = unit_vector_mp[i][1] - slope1 * unit_vector_mp[i][0]
        slope2 = perp_lines_slope[j]
        intercept2 = unit_vector_mp[j][1] - slope2 * unit_vector_mp[j][0]
        intersection = find_intersection(slope1, intercept1, slope2, intercept2)
        if intersection is not None and intersection[0] >= -15 and intersection[0] <= 15 and intersection[1] >= -15 and intersection[1] <= 15:
            intersections.append(intersection)

for i in range(len(unit_vector_mp)):
  slope = perp_lines_slope[i]
  x_intercept = unit_vector_mp[i][0]
  y_intercept = unit_vector_mp[i][1]
  x_values = np.linspace(-15, 15, 100)
  y_values = slope * (x_values - x_intercept) + y_intercept

  # SECTION: Draw the Voronoi Cell
  # WORKAROUND: Here, I somehow couldn't get atan method to work. So, I came up with this programmatic solution. 
  # This section finds two CLOSEST intersections on the same line as each midpoint and draws an orange line between them, essentially creating a voronoi cell.

  current_line_intersections = [p for p in intersections if abs((slope * (p[0] - x_intercept) + y_intercept) - p[1]) < 1e-6]
  current_line_intersections.sort(key=lambda p: p[0])
  
  closest_right = None
  closest_left = None

  for p in current_line_intersections:
      if p[0] > unit_vector_mp[i][0]:
          if closest_right is None or abs(p[0] - unit_vector_mp[i][0]) < abs(closest_right[0] - unit_vector_mp[i][0]):
              closest_right = p
      elif p[0] < unit_vector_mp[i][0]:
          if closest_left is None or abs(p[0] - unit_vector_mp[i][0]) < abs(closest_left[0] - unit_vector_mp[i][0]):
              closest_left = p
  
  if closest_left is not None and closest_right is not None and closest_left[0] <= unit_vector_mp[i][0] <= closest_right[0]:
    plt.plot([closest_left[0], closest_right[0]], [closest_left[1], closest_right[1]], '-', color="orange")
    

print("Voronoi diagram completed.")

# Set graph axes
plt.xlim(-15, 15)
plt.ylim(-15, 15)

plt.plot(0, 0, 'x', markersize=5, color='red')
plt.plot(perm_seedX[1:], perm_seedY[1:], "*", markersize=5)
plt.title("Voronoi Cell of the Origin")
plt.show()
