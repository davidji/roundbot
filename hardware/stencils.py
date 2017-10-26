from solid import *
from solid.utils import *
import util
from util import *

STENCIL_THICKNESS=0.25

class dil:
  @classmethod
  def pads(cls):
      pad = square([cls.X, cls.Y], center=True)
      return union()(*(translate([xi*cls.C, (yi - (float(cls.N)/2-1)/2)*cls.E])(pad) for yi in range(cls.N/2) for xi in (0.5, -0.5)))

  @classmethod
  def breakout_stencil(cls):
      return (linear_extrude(STENCIL_THICKNESS)(square(cls.breakout_d, center=True) - cls.pads()) +
              linear_extrude(STENCIL_THICKNESS+1.0)(square([d + 3 for d in cls.breakout_d], center=True) - square(cls.breakout_d, center=True)))

class sot23:
    Z = 3.20
    G = 1.60
    """X pad size"""
    X = 0.50
    """Y pad size"""
    Y = 0.50
    """X spacing between opposite pads"""
    C = 2.40
    """Y spacing between adjacent pads"""
    E = 0.95

    breakout_d = [10.0, 7.5]

class sot23_6(sot23, dil):
    N = 6

def export_scad():
    util.save('sot23-6-breakout-stencil', sot23_6.breakout_stencil())

if __name__ == '__main__':
    export_scad()
