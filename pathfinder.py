import heapq
import random
import math


# Update terrain costs with slight randomness
def get_terrain_cost(biome, pos, prev_pos=None):
    base_costs = {
        "o": 9999,  # Ocean (impassable)
        "w": 9999,  # Water (impassable)
        "s": 3.0,   # Swamp (very difficult)
        "b": 2.0,   # Beach
        "d": 2.5,   # Desert (difficult)
        "g": 1.0,   # Grassland (easiest)
        "h": 2.5,   # Hills
        "c": 4.0,   # Cliffs (very difficult)
        "m": 9999,  # Mountains (impassable)
        "p": 9999   # Snowy peaks (impassable)
    }

    cost = base_costs[biome]

    # Add slight randomness (±10%)
    cost *= random.uniform(0.9, 1.1)

    # If we have a previous position, penalize sharp turns
    if prev_pos:
        # Calculate direction change
        old_dx = pos[0] - prev_pos[0]
        old_dy = pos[1] - prev_pos[1]
        if old_dx != 0 or old_dy != 0:
            # Penalize 90-degree turns
            turn_penalty = 1.5 if abs(old_dx) + abs(old_dy) > 1 else 1.0
            cost *= turn_penalty

    return cost


def get_neighbors(pos, heightmap, width, height):
    # Extract just x,y if pos is a tuple with more than 2 values
    x, y = pos[:2] if len(pos) > 2 else pos

    # Include diagonal movements
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    neighbors = []
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < width and 0 <= ny < height:
            neighbors.append((nx, ny))
    return neighbors


def heuristic(a, b):
    # Extract just x,y if positions include size
    ax, ay = a[:2] if len(a) > 2 else a
    bx, by = b[:2] if len(b) > 2 else b
    
    # Using diagonal distance for more natural paths
    dx = abs(ax - bx)
    dy = abs(ay - by)
    return max(dx, dy) + 0.5 * min(dx, dy)


def a_star(start, goal, heightmap, get_biome, width, height):
    start = start[:2] if len(start) > 2 else start
    goal = goal[:2] if len(goal) > 2 else goal

    open_set = []
    heapq.heappush(open_set, (0, start))

    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            return reconstruct_path(came_from, current)

        prev_pos = came_from.get(current)

        for neighbor in get_neighbors(current, heightmap, width, height):
            biome = get_biome(heightmap[neighbor[0]][neighbor[1]])
            # Update impassable terrain types
            if biome in ["o", "w", "m", "p"]:
                continue

            tentative_g_score = g_score[current] + get_terrain_cost(
                biome, neighbor, prev_pos
            )

            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return []


# Reconstruct the path from A* results
def reconstruct_path(came_from, current):
    path = []
    while current in came_from:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path
