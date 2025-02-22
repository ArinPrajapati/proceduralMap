import random


def place_villages(
    heightmap, width, height, get_biome, num_villages=5, min_spacing=100
):
    village_candidates = [
        (x, y)
        for y in range(5, height - 5)
        for x in range(5, width - 5)
        if get_biome(heightmap[x, y])
        in ["g", "h", "b", "d"]  # Added desert as valid location
    ]

    villages = []
    while len(villages) < num_villages and village_candidates:
        x, y = random.choice(village_candidates)
        if all(abs(x - vx) + abs(y - vy) >= min_spacing for vx, vy, _ in villages):
            # Assign a size category: 1 (small), 2 (medium), 3 (large)
            size = random.choices([1, 2, 3], weights=[0.5, 0.3, 0.2])[0]
            villages.append((x, y, size))

    return villages
