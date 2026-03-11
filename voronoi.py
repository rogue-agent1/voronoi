#!/usr/bin/env python3
"""voronoi - Voronoi diagram via Fortune's algorithm (simplified) + ASCII visualization.

Usage: python voronoi.py [--points N] [--width W] [--height H]
"""
import sys, math, random

def nearest_site(x, y, sites):
    best, best_d = 0, float('inf')
    for i, (sx, sy) in enumerate(sites):
        d = (x-sx)**2 + (y-sy)**2
        if d < best_d:
            best, best_d = i, d
    return best

def voronoi_ascii(sites, width=60, height=30):
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    grid = []
    for row in range(height):
        line = []
        y = row / height
        for col in range(width):
            x = col / width
            site_idx = nearest_site(x, y, sites)
            line.append(chars[site_idx % len(chars)])
        grid.append("".join(line))
    # mark sites
    for i, (sx, sy) in enumerate(sites):
        col = int(sx * width)
        row = int(sy * height)
        if 0 <= row < height and 0 <= col < width:
            line = list(grid[row])
            line[col] = '*'
            grid[row] = "".join(line)
    return "\n".join(grid)

def delaunay_edges(sites):
    """Brute-force Delaunay: edge (i,j) exists if some circle through i,j contains no other point."""
    n = len(sites)
    edges = set()
    for i in range(n):
        for j in range(i+1, n):
            # Check if i,j are Delaunay neighbors (share a Voronoi edge)
            # Use: for each other point k, check if circumcircle of i,j,k contains no other points
            is_edge = False
            for k in range(n):
                if k == i or k == j: continue
                ax, ay = sites[i]; bx, by = sites[j]; cx, cy = sites[k]
                D = 2*(ax*(by-cy)+bx*(cy-ay)+cx*(ay-by))
                if abs(D) < 1e-10: continue
                ux = ((ax*ax+ay*ay)*(by-cy)+(bx*bx+by*by)*(cy-ay)+(cx*cx+cy*cy)*(ay-by))/D
                uy = ((ax*ax+ay*ay)*(cx-bx)+(bx*bx+by*by)*(ax-cx)+(cx*cx+cy*cy)*(bx-ax))/D
                r2 = (ax-ux)**2+(ay-uy)**2
                valid = True
                for m in range(n):
                    if m in (i,j,k): continue
                    mx, my = sites[m]
                    if (mx-ux)**2+(my-uy)**2 < r2 - 1e-10:
                        valid = False; break
                if valid:
                    is_edge = True; break
            if is_edge or n <= 2:
                edges.add((i,j))
    return edges

def main():
    n, w, h = 8, 60, 25
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--points" and i+1 < len(args): n = int(args[i+1]); i += 2
        elif args[i] == "--width" and i+1 < len(args): w = int(args[i+1]); i += 2
        elif args[i] == "--height" and i+1 < len(args): h = int(args[i+1]); i += 2
        else: i += 1
    sites = [(random.random(), random.random()) for _ in range(n)]
    print(f"Voronoi diagram with {n} sites (* = site):\n")
    print(voronoi_ascii(sites, w, h))
    print(f"\nSites: {[(f'{x:.2f}',f'{y:.2f}') for x,y in sites]}")
    if n <= 20:
        edges = delaunay_edges(sites)
        print(f"Delaunay edges ({len(edges)}): {sorted(edges)}")

if __name__ == "__main__":
    main()
