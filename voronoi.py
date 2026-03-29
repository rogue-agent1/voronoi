#!/usr/bin/env python3
"""Voronoi Diagram - Generate Voronoi regions for 2D point sets."""
import sys, math, random

def nearest_site(x, y, sites):
    best = None; best_d = float('inf')
    for i, (sx, sy) in enumerate(sites):
        d = (x-sx)**2 + (y-sy)**2
        if d < best_d: best_d = d; best = i
    return best

def voronoi_grid(sites, width=60, height=30):
    grid = [[0]*width for _ in range(height)]
    for y in range(height):
        for x in range(width):
            grid[y][x] = nearest_site(x * 100 / width, y * 100 / height, sites)
    return grid

def render(grid, sites, width, height):
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    site_coords = set()
    for i, (sx, sy) in enumerate(sites):
        gx = int(sx * width / 100); gy = int(sy * height / 100)
        site_coords.add((gy, gx, i))
    lines = []
    for y in range(height):
        row = ""
        for x in range(width):
            is_site = False
            for sy, sx, si in site_coords:
                if sy == y and sx == x: row += "●"; is_site = True; break
            if not is_site:
                c = grid[y][x]
                is_border = False
                for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)]:
                    ny, nx = y+dy, x+dx
                    if 0<=ny<height and 0<=nx<width and grid[ny][nx] != c: is_border = True; break
                row += "·" if is_border else chars[c % len(chars)]
            
        lines.append(row)
    return "\n".join(lines)

def main():
    random.seed(42)
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    sites = [(random.randint(5,95), random.randint(5,95)) for _ in range(n)]
    w, h = 60, 25
    grid = voronoi_grid(sites, w, h)
    print(f"=== Voronoi Diagram ({n} sites) ===\n")
    print(render(grid, sites, w, h))
    print(f"\nSites:")
    for i, (x, y) in enumerate(sites): print(f"  {chr(65+i)}: ({x}, {y})")

if __name__ == "__main__":
    main()
