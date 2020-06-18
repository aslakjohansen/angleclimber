#!/usr/bin/env python3

import cairo
from math import ceil

SCALE = 72.0*2.54
MM2POINTS = 72.0/25.4
CM2POINTS = 72.0/2.54

filename = 'result.pdf'

points = list(map(lambda p: (float(p[0]), float(p[1]), float(p[2])), [
    (0, 0  , 1),
    (0, 1.2, 1),
    (0, 2.4, 1),
    (0, 3.6, 1),
]))
pos = (1.8, 5.0)

#

def cm (value):
    return float(value)/2.54*72

def mm (value):
    return cm(float(value)/10)

#

width  = 8+2
height = 3.6+2*1.2
x_offset = 1
y_offset = 1.2

surface = cairo.PDFSurface(filename, cm(width), cm(height))
c = cairo.Context(surface)
c.scale(CM2POINTS, CM2POINTS)
c.translate(0, height)
c.scale(1, -1)
c.set_line_width(0.01)

# draw grid
for x in range(0, ceil(width-x_offset)+1):
    if x>width-x_offset: continue
    c.save()
    c.move_to(x+x_offset, y_offset)
    c.line_to(x+x_offset, height-y_offset)
    c.set_source_rgb(0, 0, 0)
    c.stroke()
    c.restore()
for y in range(0, ceil(height-y_offset)+1):
    if y>height-2*y_offset: continue
    c.save()
    c.move_to(x_offset      , y+y_offset)
    c.line_to(width-x_offset, y+y_offset)
    c.set_source_rgb(0, 0, 0)
    c.stroke()
    c.restore()
    

