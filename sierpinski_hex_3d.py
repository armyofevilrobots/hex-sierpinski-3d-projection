from typing import Any

from solid import *
from solid.utils import *
from math import sin, cos, sqrt

pagesize = "letter"
order = 4
size = 100
fillet_size = 0.75

dtr = pi / 180


def chopped_cube(size, fillet=True):
    return intersection()(
        cube(1.0 * size + fillet_size, center=True),
        rotate([45, 0, 0])(cube(size * sqrt(2) - fillet_size, center=True)),
        rotate([0, 45, 0])(cube(size * sqrt(2) - fillet_size, center=True)),
        rotate([0, 0, 45])(cube(size * sqrt(2) - fillet_size, center=True))
    )

def compose(size, order):
    children = list()
    smux = 1.001  # + (0.01**order)
    for direction in [
        (0.5, 0.5, -0.5),
        (0.5, -0.5, 0.5),
        (-0.5, 0.5, 0.5)
    ]:
        if order == 0:
            pass
            children.append(
                translate([(i * size) for i in direction])(
                    chopped_cube(smux*size, True)))
        else:
            children.append(
                translate([(i * size) for i in direction])(
                    compose(smux*size/2, order-1)))
    for direction in [
        (-0.5, -0.5, 0.5),
        (-0.5, -0.5, -0.5),
        (-0.5, 0.5, -0.5),
        (0.5, -0.5, -0.5),
    ]:
        children.append(translate([(i*size) for i in direction])(
                chopped_cube(smux*size, True)))

    return union()(*children)


def decompose(parent, size, order):
    """Takes a cube, and decomposes it into the cube with three chunks removed.
    Algo:
    Calculate front corner (+Z), left,right, top,bottom (etc.)
    At +X +Y +Z corner, define the starting point.
    for dir in xy,yz,xz:
        define a cube "child" to subtract from parent at start-dir*(0.5, 0.5, 0.5)
        children[dir] = decompose(child, size/2, order-1)
    return difference(parent, children)
    """
    print(parent.params)
    children = list()
    smux = 1.0
    # smux = 0.999 ** order
    front = translate([0.505*size, 0.505*size, 0.505*size])(cube(smux*size, True))
    for direction in [(0.505, 0.505, -0.495),
                      (0.505, -0.495, 0.505),
                      (-0.495, 0.505, 0.505)]:
        if order > 0:
            child = difference()(translate([(i*size) for i in direction])(
                cube(smux*size, True)),
                translate([(i*size) for i in direction])(
                    decompose(cube(smux*size, True), smux*size / 2, order - 1)))
        else:
            child = translate([(i*size) for i in direction])(cube(smux*size, True))
        children.append(child)
    return difference()(parent, front, *children)


if __name__ == "__main__":
    # top = decompose(cube(size, center=True), size/2, order)
    top = compose(size, order)
    scad_render_to_file(top, "sierpinski_hex_3d.scad")