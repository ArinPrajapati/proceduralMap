import matplotlib
import numpy as np
import matplotlib.pyplot as plt 
import noise

matplotlib.use("TkAgg")

# map dimensions 
width,height = 100,100
scale = 10.0
octaves = 8
persistence = 0.5
lacunarilty = 2.0
heightmap = np.zeros((width,height))


for y in range(height):
    for x in range(width):
        heightmap[x][y] = noise.pnoise2(x/scale,y/scale,octaves=octaves,persistence= persistence , lacunarity=lacunarilty , repeatx=width, repeaty=height, base=42)

min_val, max_val = np.min(heightmap), np.max(heightmap)
heightmap = (heightmap - min_val) / (max_val - min_val) 



plt.imshow(heightmap,cmap="gray",origin="upper")
plt.colorbar(label ="height value")
plt.title("perlin noise heightmap")
plt.show()
