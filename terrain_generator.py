import noise
import numpy as np
import random


def generate_heightmap(
    width, height, scale=100.0, octaves=80, persistence=0.5, lacunarity=2.0, seed=random.randint(0, 1000)
):
    heightmap = np.zeros((width, height))

    for y in range(height):
        for x in range(width):
            heightmap[x][y] = noise.pnoise2(
                x / scale,
                y / scale,
                octaves=octaves,
                persistence=persistence,
                lacunarity=lacunarity,
                repeatx=width,
                repeaty=height,
                base=seed,
            )

    # Normalize the heightmap
    min_val, max_val = np.min(heightmap), np.max(heightmap)
    heightmap = (heightmap - min_val) / (max_val - min_val)

    return heightmap


def get_biome(value):
    if value < 0.2:
        return "o"  # Ocean
    elif value < 0.3:
        return "w"  # Shallow water
    elif value < 0.35:
        return "s"  # Swamp
    elif value < 0.4:
        return "b"  # Beach
    elif value < 0.45:
        return "d"  # Desert
    elif value < 0.6:
        return "g"  # Grasslands
    elif value < 0.75:
        return "h"  # Hills
    elif value < 0.85:
        return "c"  # Cliffs
    elif value < 0.95:
        return "m"  # Mountains
    else:
        return "p"  # Snowy peaks
