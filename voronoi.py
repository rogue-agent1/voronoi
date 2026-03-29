#!/usr/bin/env python3
"""voronoi - Voronoi diagram via brute-force nearest-site assignment."""
import sys, math

def assign_sites(points, width, height, resolution=1):
    grid = {}
    for y in range(0, height, resolution):
        for x in range(0, width, resolution):
            min_d = float('inf')
            nearest = -1
            for i, (px, py) in enumerate(points):
                d = (x - px)**2 + (y - py)**2
                if d < min_d:
                    min_d = d
                    nearest = i
            grid[(x, y)] = nearest
    return grid

def cell_areas(grid, resolution=1):
    areas = {}
    for _, site in grid.items():
        areas[site] = areas.get(site, 0) + resolution * resolution
    return areas

def neighbors(grid, num_sites):
    adj = {i: set() for i in range(num_sites)}
    for (x, y), s in grid.items():
        for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            n = grid.get((x+dx, y+dy))
            if n is not None and n != s:
                adj[s].add(n)
                adj[n].add(s)
    return {k: sorted(v) for k, v in adj.items()}

def test():
    pts = [(10, 10), (30, 10), (20, 30)]
    grid = assign_sites(pts, 40, 40)
    assert len(grid) == 40 * 40
    assert grid[(10, 10)] == 0
    assert grid[(30, 10)] == 1
    assert grid[(20, 30)] == 2
    areas = cell_areas(grid)
    assert sum(areas.values()) == 40 * 40
    assert len(areas) == 3
    nbrs = neighbors(grid, 3)
    # all three cells should be neighbors of each other
    assert 1 in nbrs[0] and 2 in nbrs[0]
    print("OK: voronoi")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test()
    else:
        print("Usage: voronoi.py test")
