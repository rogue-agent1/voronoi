#!/usr/bin/env python3
"""Voronoi diagram (ASCII)."""
import sys, random, math
n=int(sys.argv[1]) if len(sys.argv)>1 else 8
w,h=60,30
random.seed(42)
seeds=[(random.randint(0,w-1),random.randint(0,h-1)) for _ in range(n)]
chars='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
for r in range(h):
    row=''
    for c in range(w):
        closest=min(range(n),key=lambda i:math.hypot(c-seeds[i][0],r-seeds[i][1]))
        row+=chars[closest%len(chars)]
    print(row)
print(f"\n{n} regions, {w}x{h}")
