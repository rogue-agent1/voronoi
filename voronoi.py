#!/usr/bin/env python3
"""voronoi - Voronoi diagram generator with ASCII output."""
import random, math, argparse

def voronoi(w, h, seeds, seed_val=None):
    if seed_val is not None: random.seed(seed_val)
    points = [(random.randint(0,w-1), random.randint(0,h-1)) for _ in range(seeds)]
    grid = [[0]*w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            best = float("inf"); bi = 0
            for i,(px,py) in enumerate(points):
                d = (x-px)**2 + (y-py)**2
                if d < best: best = d; bi = i
            grid[y][x] = bi
    return grid, points

def render(grid, points):
    syms = "abcdefghijklmnopqrstuvwxyz0123456789"
    lines = []
    ps = {(px,py) for px,py in points}
    for y, row in enumerate(grid):
        line = ""
        for x, c in enumerate(row):
            if (x,y) in ps: line += "*"
            else: line += syms[c % len(syms)]
        lines.append(line)
    return "\n".join(lines)

def main():
    p = argparse.ArgumentParser(description="Voronoi diagram generator")
    p.add_argument("-W", type=int, default=60); p.add_argument("-H", type=int, default=25)
    p.add_argument("-n", "--seeds", type=int, default=8)
    p.add_argument("--seed", type=int, default=None)
    args = p.parse_args()
    grid, points = voronoi(args.W, args.H, args.seeds, args.seed)
    print(render(grid, points))

if __name__ == "__main__":
    main()
