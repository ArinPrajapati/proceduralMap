import matplotlib
import numpy as np
import matplotlib.pyplot as plt 
import noise
import time
import random
matplotlib.use("TkAgg")

width, height = 1000, 1000
scale = 100.0
octaves = 80
persistence = 0.5
lacunarilty = 2.0
heightmap = np.zeros((width, height))

for y in range(height):
    for x in range(width):
        heightmap[x][y] = noise.pnoise2(
            x / scale, y / scale, 
            octaves=octaves, 
            persistence=persistence, 
            lacunarity=lacunarilty, 
            repeatx=width, 
            repeaty=height, 
            base=42
        )

min_val, max_val = np.min(heightmap), np.max(heightmap)
heightmap = (heightmap - min_val) / (max_val - min_val) 

# Biome classification function
def get_biome(value):
    if value < 0.3:  
        return "w"  # Water
    elif value < 0.4:  
        return "b"  # Beach
    elif value < 0.6:  
        return "g"  # Grasslands
    elif value < 0.8:  
        return "h"  # Hills
    else:  
        return "m"  # Mountains

village_candidates = [
    (x, y) for y in range(5, height - 5)
    for x in range(5, width - 5)
    if get_biome(heightmap[x, y]) in ["g", "h", "b"]
]

num_village = 5
villages = []
min_spacing = 100

while len(villages) < num_village and village_candidates:
    x, y = random.choice(village_candidates)
    if all(abs(x - vx) + abs(y - vy) >= min_spacing for vx, vy in villages):
        villages.append((x, y))

biome_map = np.zeros((width, height, 3))
biome_colors = {
    "w": [0, 0, 1],  # Blue (Water)
    "b": [0.9, 0.8, 0.5],  # Yellow (Beach)
    "g": [0, 0.8, 0],  # Green (Grassland)
    "h": [0.5, 0.4, 0.2],  # Brown (Hills)
    "m": [1, 1, 1]  # White (Mountains)
}

for y in range(height):
    for x in range(width):
        biome_map[x, y] = biome_colors[get_biome(heightmap[x, y])]

for x, y in villages:
    for dx in range(-3, 4):  # Spread over a 7x7 area
        for dy in range(-3, 4):
            if 0 <= x + dx < width and 0 <= y + dy < height:
                biome_map[x + dx, y + dy] = [1, 0, 0]  # Red for villages

plt.figure(figsize=(10, 10))
plt.imshow(heightmap, cmap="gray", origin="upper")
plt.colorbar(label="Height Value")
plt.title("Perlin Noise Heightmap")
plt.show()

plt.figure(figsize=(10, 10))
plt.imshow(biome_map, origin="upper")
plt.title("Procedural Terrain with Biomes & Villages")
plt.axis("off")
plt.show()

filename = f"biome_map_{int(time.time())}.png"
plt.imsave(filename, biome_map)
print(f"Biome map saved as {filename}")

