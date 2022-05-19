#!/usr/bin/env python3

import math

def move_point(xy, rt):
    xy[0] += rt[0] * math.cos(rt[1])
    xy[1] += rt[0] * math.sin(rt[1])

    return xy

polar = [1., 0.]
cartesian = [200, 150]

print(polar, cartesian)

for i in range(0, 31):
    polar[1] += math.pi * 0.01
    print(move_point(cartesian, polar))
    print(polar, cartesian)
