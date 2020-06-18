#!/usr/bin/env python3

import cairo
from math import ceil, pi, sin

SCALE = 72.0*2.54
MM2POINTS = 72.0/25.4
CM2POINTS = 72.0/2.54

filename = 'result.pdf'

points = list(map(lambda p: (float(p[0]), float(p[1]), float(p[2])), [
    (0, 0  ,  20.183827),
    (0, 1.2,   6.859004),
    (0, 2.4,  -6.859004),
    (0, 3.6, -20.183827),
]))
pos = (5.0, 1.8)

steps = []

#

def cm (value):
    return float(value)/2.54*72

def mm (value):
    return cm(float(value)/10)

def rad2deg (rad):
    return float(rad/(2*pi)*360)

def print_true_angles ():
    for point in points:
        dx = pos[0]-point[0]
        dy = pos[1]-point[1]
        angle = rad2deg(sin(float(dy)/dx))
        print('Angle: %f' % angle)

def plot_point (c, x, y, r, g, b):
    c.save()
    c.arc(x, y, .1, 0, 2*pi);
    c.set_source_rgba(r, g, b, 0.2)
    c.fill_preserve()
    c.set_source_rgb(r, g, b)
    c.stroke()
    c.restore()

#

width  = 8+2
height = 3.6+2*1.2
x_offset = 1
y_offset = 1.2

surface = cairo.PDFSurface(filename, cm(width), cm(height))
c = cairo.Context(surface)
c.scale(CM2POINTS, CM2POINTS)
c.translate(x_offset, height-y_offset)
c.scale(1, -1)
c.set_line_width(0.01)

# draw grid
for x in range(0, ceil(width-x_offset)+1):
    if x>width-x_offset: continue
    c.save()
    c.move_to(x, 0)
    c.line_to(x, height-y_offset*2)
    c.set_source_rgb(0, 0, 0)
    c.stroke()
    c.restore()
for y in range(0, ceil(height-y_offset)+1):
    if y>height-2*y_offset: continue
    c.save()
    c.move_to(0               , y)
    c.line_to(width-x_offset*2, y)
    c.set_source_rgb(0, 0, 0)
    c.stroke()
    c.restore()

# plot points
for point in points:
    plot_point(c, point[0], point[1], 0,0,1)
plot_point(c, pos[0], pos[1], 1,0,0)

print_true_angles()

