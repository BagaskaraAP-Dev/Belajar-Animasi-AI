import sys, cairo
from scenes import *
for ts in sys.argv[1:]:
    t=float(ts)
    s=cairo.ImageSurface(cairo.FORMAT_ARGB32,W,H); c=cairo.Context(s)
    frame(c,t); s.write_to_png(f'f_{ts}.png')
