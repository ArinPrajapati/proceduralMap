import matplotlib

matplotlib.use("TkAgg")

from terrain_generator import generate_heightmap, get_biome
from village_placer import place_villages
from map_renderer import (
    create_biome_map,
    draw_villages,
    draw_roads,
    save_and_display_maps,
)
from roadbuilding import build_road
from water_systems import create_river_system
from map_renderer import draw_rivers


def main():
    # Map dimensions
    width, height = 1000, 1000

    # Generate terrain
    heightmap = generate_heightmap(width, height)

    # Place villages
    villages = place_villages(heightmap, width, height, get_biome, num_villages=10)

    # Create and populate biome map
    biome_map = create_biome_map(heightmap, get_biome, width, height)

    # Generate rivers and lakes
    rivers, lakes = create_river_system(heightmap, get_biome, biome_map)

    # Draw rivers
    draw_rivers(biome_map, rivers, width, height)

    # Draw villages (after rivers so they don't get overwritten)
    draw_villages(biome_map, villages, width, height)

    # Build and draw roads
    roads = build_road(villages, villages[-1], heightmap, width, height, get_biome)
    draw_roads(biome_map, roads, width, height)

    # Display and save the results
    save_and_display_maps(heightmap, biome_map)


if __name__ == "__main__":
    main()
