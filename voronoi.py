#!/usr/bin/env python3
"""voronoi: Voronoi diagram via brute-force nearest-site assignment."""
import math, sys

def nearest_site(point, sites):
    best_i, best_d = 0, float('inf')
    for i, s in enumerate(sites):
        d = math.sqrt((point[0]-s[0])**2 + (point[1]-s[1])**2)
        if d < best_d:
            best_i, best_d = i, d
    return best_i

def voronoi_grid(sites, width, height, resolution=1):
    grid = []
    for y in range(0, height, resolution):
        row = []
        for x in range(0, width, resolution):
            row.append(nearest_site((x, y), sites))
        grid.append(row)
    return grid

def lloyd_relax(sites, width, height, iterations=1, resolution=1):
    sites = [list(s) for s in sites]
    for _ in range(iterations):
        grid = voronoi_grid(sites, width, height, resolution)
        centroids = {i: ([], []) for i in range(len(sites))}
        for y, row in enumerate(grid):
            for x, site_id in enumerate(row):
                centroids[site_id][0].append(x * resolution)
                centroids[site_id][1].append(y * resolution)
        for i in range(len(sites)):
            xs, ys = centroids[i]
            if xs:
                sites[i] = [sum(xs)/len(xs), sum(ys)/len(ys)]
    return [tuple(s) for s in sites]

def test():
    sites = [(10,10), (40,40), (10,40)]
    grid = voronoi_grid(sites, 50, 50)
    assert grid[0][0] == 0  # (0,0) closest to (10,10)
    assert grid[49][49] == 1  # (49,49) closest to (40,40)
    assert grid[49][0] == 2  # (0,49) closest to (10,40)
    # Lloyd relaxation
    new_sites = lloyd_relax(sites, 50, 50, iterations=3)
    assert len(new_sites) == 3
    # Sites should spread more evenly
    for s in new_sites:
        assert 0 <= s[0] <= 50
        assert 0 <= s[1] <= 50
    # Single site
    grid2 = voronoi_grid([(25,25)], 50, 50)
    assert all(cell == 0 for row in grid2 for cell in row)
    print("All tests passed!")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test": test()
    else: print("Usage: voronoi.py test")
