import argparse, random, math

def voronoi(width, height, n_points, seed=None):
    if seed: random.seed(seed)
    points = [(random.randint(0, width-1), random.randint(0, height-1)) for _ in range(n_points)]
    chars = "·#@%&*+=$~"
    grid = []
    for y in range(height):
        row = ""
        for x in range(width):
            min_dist = float("inf")
            closest = 0
            for i, (px, py) in enumerate(points):
                d = math.sqrt((x-px)**2 + (y-py)**2)
                if d < min_dist: min_dist = d; closest = i
            row += chars[closest % len(chars)]
        grid.append(row)
    # Mark points
    grid_list = [list(row) for row in grid]
    for px, py in points:
        if 0 <= py < height and 0 <= px < width:
            grid_list[py][px] = "●"
    return ["".join(row) for row in grid_list]

def main():
    p = argparse.ArgumentParser(description="Voronoi diagram")
    p.add_argument("-w", "--width", type=int, default=60)
    p.add_argument("-H", "--height", type=int, default=25)
    p.add_argument("-n", "--points", type=int, default=8)
    p.add_argument("--seed", type=int)
    p.add_argument("--manhattan", action="store_true")
    args = p.parse_args()
    grid = voronoi(args.width, args.height, args.points, args.seed)
    for row in grid: print(row)

if __name__ == "__main__":
    main()
