#!/usr/bin/env python3

import cairo
from math import ceil, pi, sin, sqrt

SCALE = 72.0*2.54
MM2POINTS = 72.0/25.4
CM2POINTS = 72.0/2.54

filename = 'result.pdf'
threshold = .1
stepsize  = .01

points = list(map(lambda p: (float(p[0]), float(p[1]), float(p[2])), [
    (0, 0  ,  20.183827),
    (0, 1.2,   6.859004),
    (0, 2.4,  -6.859004),
    (0, 3.6, -20.183827),
]))
pos_true = (5.0, 1.8)
pos      = (7,3, 0.2)

steps = []

#

def cm (value):
    return float(value)/2.54*72

def mm (value):
    return cm(float(value)/10)

def rad2deg (rad):
    return float(rad/(2*pi)*360)

def calcangle (pos, point):
    dx = pos[0]-point[0]
    dy = pos[1]-point[1]
    return rad2deg(sin(float(dy)/dx))

def print_true_angles ():
    for point in points:
#        dx = pos_true[0]-point[0]
#        dy = pos_true[1]-point[1]
#        angle = rad2deg(sin(float(dy)/dx))
        angle = calcangle(pos_true, point)
        print('Angle: %f' % angle)

def plot_point (c, x, y, r, g, b):
    c.save()
    c.arc(x, y, .1, 0, 2*pi);
    c.set_source_rgba(r, g, b, 0.2)
    c.fill_preserve()
    c.set_source_rgb(r, g, b)
    c.stroke()
    c.restore()

def calc_badness (pos):
    return sqrt(sum(map(lambda p: sqrt((calcangle(pos, p)-p[2])**2), points)))

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
plot_point(c, pos_true[0], pos_true[1], 0,1,0)
plot_point(c, pos[0], pos[1], 1,0,0)

print_true_angles()

badness = calc_badness(pos)
steps.append({'x': pos[0], 'y': pos[1], 'b': badness})
ttl = 100000
while badness>threshold and ttl>0:
    for direction, diff in [('x', 1), ('x', -1), ('y', 1), ('y', -1)]:
        newpos = (
            pos[0]+(stepsize*diff if direction=='x' else 0),
            pos[1]+(stepsize*diff if direction=='y' else 0)
        )
        new_badness = calc_badness(newpos)
        
        if new_badness<badness:
            pos = newpos
            badness = new_badness
            steps.append({'x': pos[0], 'y': pos[1], 'b': badness})
        
        ttl -= 1

print(pos)
#print(steps)

for i in range(len(steps)-1):
    p1 = steps[i]
    p2 = steps[i+1]
    
    c.save()
    c.move_to(p1['x'], p1['y'])
    c.line_to(p2['x'], p2['y'])
    c.set_source_rgb(1, 0, 0)
    c.stroke()
    c.restore()

