from pathfinder import a_star
import sys

def build_road(villages, goal, heightmap, width, height, get_biome):
    all_roads = set()
    connected = {villages[0]}
    unconnected = set(villages[1:])
    
    print("Building roads...")
    total_connections = len(villages) - 1
    current_connection = 0
    
    while unconnected:
        best_path = None
        best_distance = float('inf')
        best_start = None
        best_end = None
        
        # Find the shortest path from any connected village to any unconnected village
        for start in connected:
            for end in unconnected:
                path = a_star(start, end, heightmap, get_biome, width, height)
                if path and len(path) < best_distance:
                    best_path = path
                    best_distance = len(path)
                    best_start = start
                    best_end = end
        
        if best_path:
            all_roads.update(best_path)
            connected.add(best_end)
            unconnected.remove(best_end)
            current_connection += 1
            print(f"Road progress: {current_connection}/{total_connections}", end='\r')
            sys.stdout.flush()
        else:
            break
    
    return list(all_roads)
