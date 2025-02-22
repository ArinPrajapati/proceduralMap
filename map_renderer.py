import numpy as np
import matplotlib.pyplot as plt
import time

BIOME_COLORS = {
    "o": [0, 0, 0.7],     # Dark blue (Ocean)
    "w": [0, 0.4, 1.0],   # Light blue (Shallow water)
    "s": [0.2, 0.5, 0.2], # Dark green (Swamp)
    "b": [0.9, 0.8, 0.5], # Yellow (Beach)
    "d": [0.9, 0.8, 0.2], # Sandy yellow (Desert)
    "g": [0.2, 0.8, 0.2], # Green (Grassland)
    "h": [0.5, 0.4, 0.2], # Brown (Hills)
    "c": [0.4, 0.4, 0.4], # Gray (Cliffs)
    "m": [0.7, 0.7, 0.7], # Light gray (Mountains)
    "p": [1, 1, 1],       # White (Snowy peaks)
}


def create_biome_map(heightmap, get_biome, width, height):
    biome_map = np.zeros((width, height, 3))
    for y in range(height):
        for x in range(width):
            biome_map[x, y] = BIOME_COLORS[get_biome(heightmap[x, y])]
    return biome_map


def draw_villages(biome_map, villages, width, height):
    for x, y, size in villages:
        # Size determines the village radius
        radius = {1: 3, 2: 5, 3: 7}[size]

        # Draw the village as a circle
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                if dx * dx + dy * dy <= radius * radius:  # Circle equation
                    if 0 <= x + dx < width and 0 <= y + dy < height:
                        # Different shades of red for different sizes
                        color = {
                            1: [0.8, 0.2, 0.2],  # Light red for small
                            2: [0.9, 0.1, 0.1],  # Medium red
                            3: [1.0, 0.0, 0.0],  # Bright red for large
                        }[size]
                        biome_map[x + dx, y + dy] = color


def draw_roads(biome_map, roads, width, height):
    for x, y in roads:
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if 0 <= x + dx < width and 0 <= y + dy < height:
                    biome_map[x + dx, y + dy] = [0.5, 0.5, 0.5]  # Gray


def draw_rivers(biome_map, rivers, width, height):
    """Draw rivers on the map"""
    for x, y in rivers:
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if 0 <= x + dx < width and 0 <= y + dy < height:
                    biome_map[x + dx, y + dy] = [0, 0, 1]  # Blue for rivers


def save_and_display_maps(heightmap, biome_map):
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
