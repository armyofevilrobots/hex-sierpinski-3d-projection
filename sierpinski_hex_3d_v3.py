from typing import Any

from solid import *
from solid.utils import *
from math import sin, cos, sqrt, atan
import random
import time

orig_order = 3
order = orig_order
size = 150
post = True  # Adds a hole for a mnounting post at the back.
hole_radius = 1.5
# Calculate the angle of bottom back corner to top front corner, for the hole
cross_angle = (180 * atan(2 * size / (size * sqrt(2.0)))) / pi
probability_cut = 0.90
probability_add = 0.1
random.seed(time.time())

def decompose(x, y, z, size, order):
    """Chop out the corner, then recurse and repeat for each order"""
    subcubes = [translate((x,y,z))(cube(size, center=True))]
    addcubes = []
    for add_dir, mate_dir in [([x, y-size/2, z], [x, y-size/2, z]),
                              ([x-size/2, y, z], [x-size/2, y, z]),
                              ([x, y, z-size/2], [x, y, z-size/2])]:
        if order > 0 and random.random() < probability_cut**(orig_order-order):
            child_sub, child_add = decompose(*mate_dir, size=size/2, order=order-1)
            subcubes.extend(child_sub)
            addcubes.extend(child_add)
        elif random.random() < probability_add**(1/(orig_order-order)):
            addcubes.append(translate((x-size/2, y-size/2,z-size/2))(cube(1.0001*size/2, center=True)))
    return subcubes, addcubes


def compose(size: float, order: int):
    """New simpler compose that just generates a cube with only cutouts."""
    base = cube(size, center=True)
    subtract_cubes, add_cubes = decompose(size/2, size/2, size/2, size, order)
    print(len(subtract_cubes), len(add_cubes))
    return union()(difference()(base, *subtract_cubes), *add_cubes)


if __name__ == "__main__":
    # top = decompose(cube(size, center=True), size/2, order)

    if post:
        top = difference()(compose(size, order),
                           translate((-size/2, -size/2, -size/2))(
                          rotate((0, 0, 45))(
                              rotate((0, cross_angle, 0))(
                                  cylinder(r=hole_radius, h=60, center=True, segments=8)))))
    else:
        top = compose(size, order)
    scad_render_to_file(top, f"sierpinski_hex_3d_v3_{size}mm_ord{order}_{probability_cut}.scad")