import matplotlib
import numpy as np
import matplotlib.pyplot as plt 
import noise
import time
matplotlib.use("TkAgg")

# map dimensions 
width,height = 1000,1000
scale = 100.0
octaves = 80
persistence = 0.5
lacunarilty = 2.0
heightmap = np.zeros((width,height))


for y in range(height):
    for x in range(width):
        heightmap[x][y] = noise.pnoise2(x/scale,y/scale,octaves=octaves,persistence= persistence , lacunarity=lacunarilty , repeatx=width, repeaty=height, base=42)

min_val, max_val = np.min(heightmap), np.max(heightmap)
heightmap = (heightmap - min_val) / (max_val - min_val) 

def get_biome_color(value):
    if value < 0.3: # water
        return [0,0,1]#blue 
    elif value < 0.4: # beach 
        return [0.9,0.8,0.5] # sandys yellow
    elif value < 0.6: # grasslands
        return [0,0.8,0] # green 
    elif value < 0.8: #hills
        return [0.5,0.4,0.2]#brown
    else: #mounatins
        return [1,1,1] # white

biome_map = np.zeros((width,height,3))

for y in range(height):
    for x in range(width):
        biome_map[x,y] = get_biome_color(heightmap[x,y])

plt.imshow(heightmap,cmap="gray",origin="upper")
plt.colorbar(label ="height value")
plt.title("perlin noise heightmap")

plt.show()

plt.imshow(biome_map,origin="upper")
plt.title("PT with Biome")
plt.axis("off")


filename = f"plot_{int(time.time())}.png"

plt.savefig(filename)
