import numpy as np
import random
from collections import deque
import sys

def find_mountain_sources(heightmap, get_biome, num_sources=5):
    """Find mountain peaks to serve as river sources"""
    print("Finding mountain sources...")
    width, height = heightmap.shape
    mountain_sources = []
    
    # Find all mountain tiles
    mountains = [
        (x, y) for x in range(width) for y in range(height)
        if get_biome(heightmap[x, y]) == "m"
    ]
    
    # Select random mountain peaks as sources
    if mountains:
        mountain_sources = random.sample(mountains, min(num_sources, len(mountains)))
        print(f"Found {len(mountain_sources)} mountain sources")
    else:
        print("Warning: No mountain sources found")
    
    return mountain_sources

def get_flow_direction(x, y, heightmap, width, height):
    """Determine the direction of water flow based on height differences"""
    current_height = heightmap[x, y]
    directions = [(dx, dy) for dx in [-1,0,1] for dy in [-1,0,1] if dx != 0 or dy != 0]
    
    # Find the steepest downhill direction
    min_height = current_height
    flow_dir = None
    
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < width and 0 <= ny < height:
            if heightmap[nx, ny] < min_height:
                min_height = heightmap[nx, ny]
                flow_dir = (nx, ny)
    
    return flow_dir

def create_river_system(heightmap, get_biome, biome_map):
    """Generate rivers and lakes"""
    width, height = heightmap.shape
    sources = find_mountain_sources(heightmap, get_biome)
    rivers = set()
    lakes = set()
    
    print("\nGenerating river systems...")
    total_sources = len(sources)
    
    for idx, source in enumerate(sources, 1):
        current_pos = source
        river_path = set()
        
        print(f"Creating river {idx}/{total_sources} from source at {source}", end='\r')
        sys.stdout.flush()
        
        while current_pos:
            x, y = current_pos
            river_path.add(current_pos)
            
            # Check if we've reached water
            if get_biome(heightmap[x, y]) in ["o", "w", "b"]:
                rivers.update(river_path)
                break
                
            # Get next position based on height
            next_pos = get_flow_direction(x, y, heightmap, width, height)
            
            # If no downstream flow is found, create a lake
            if not next_pos or next_pos in river_path:
                lakes.add(current_pos)
                print(f"\nCreating lake at {current_pos}...")
                spread_lake(current_pos, heightmap, biome_map, width, height)
                rivers.update(river_path)
                break
                
            current_pos = next_pos
    
    print(f"\nWater system complete! Created {len(rivers)} river tiles and {len(lakes)} lakes")
    return rivers, lakes

def spread_lake(center, heightmap, biome_map, width, height):
    """Spread a lake around the given center point"""
    lake_cells = set()
    queue = deque([center])
    radius = random.randint(3, 7)
    
    while queue:
        x, y = queue.popleft()
        
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                nx, ny = x + dx, y + dy
                if (0 <= nx < width and 0 <= ny < height and
                    (nx-center[0])**2 + (ny-center[1])**2 <= radius**2 and
                    (nx, ny) not in lake_cells):
                    lake_cells.add((nx, ny))
                    queue.append((nx, ny))
                    biome_map[nx, ny] = [0, 0, 0.8]  # Lighter blue for lakes