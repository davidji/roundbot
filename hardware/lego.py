from solid import *
from solid.utils import *

"""most lego dimentions are in terms of a unit, which is 1.6mm"""
from solid.solidpython import linear_extrude
unit=1.6
"""This is the stud pitch"""
pitch=8.0
tolerance=0.1

def stud():
    return linear_extrude(unit)(circle(d=3*unit))

def studs_center(x_studs, y_studs, center):
    return translate(center and [-(((x_studs-1)*pitch)/2), -(((y_studs-1)*pitch)/2)] or [pitch/2, pitch/2])

def studs(x_studs,y_studs,center=True):
    row = union()(*(right(pos*pitch)(stud()) for pos in range(x_studs)))
    grid = union()(*(forward(pos*pitch)(row) for pos in range(y_studs)))
    return studs_center(x_studs, y_studs, center)(grid)

def surface(x_studs,y_studs,center=True):
    return square([x_studs*pitch + tolerance, y_studs*pitch + tolerance], center=center)
