import sys, os, subprocess, cairo
from scenes import *
name, f0, f1 = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
tmp = f'{name}.tmp.mp4'
p = subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','bgra','-s',f'{W}x{H}','-r',str(FPS),
    '-i','-','-c:v','libx264','-crf','18','-preset','veryfast','-pix_fmt','yuv420p','-r',str(FPS),tmp], stdin=subprocess.PIPE)
s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
for f in range(f0, f1):
    c = cairo.Context(s)
    c.set_source_rgb(0,0,0); c.paint()
    frame(c, f / FPS)
    s.flush()
    p.stdin.write(bytes(s.get_data()))
p.stdin.close()
if p.wait() == 0:
    os.replace(tmp, f'{name}.mp4')
else:
    sys.exit(1)
