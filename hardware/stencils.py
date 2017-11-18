from solid import *
from solid.utils import *
import util
from util import *

STENCIL_THICKNESS=0.25
BREAKOUT_THICKNESS = 1.6
TOLERANCE=0.4

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
    breakout_t = 1.6

class soic:
    """X pad size"""
    X = 2.25
    """Y pad size"""
    Y = 0.50
    """X spacing between opposite pads"""
    C = 4.65
    """Y spacing between adjacent pads"""
    E = 1.27
    
class stencil:
    stencil_d=[22.84,33.0]
    stencil_offset = [0.0, 0.0]
    
    @classmethod
    def breakout_stencil_shim(cls):
        return (
            linear_extrude(
                cls.breakout_t+1.0)(
                    offset(r=2.0)(square(cls.stencil_d, center=True))) -
                up(cls.breakout_t)(linear_extrude(1.0)(
                    offset(delta=TOLERANCE)(square(cls.stencil_d, center=True)) +
                    square([cls.stencil_d[0] + 4, cls.stencil_d[1] -2 ], center=True))) -
                linear_extrude(cls.breakout_t)(
                    translate(cls.stencil_offset)(
                        offset(delta=TOLERANCE)(square(cls.breakout_d, center=True)) +
                        back(cls.breakout_d[1]/2)(circle(d=cls.breakout_d[0] - 2)) +
                        forward(cls.breakout_d[1]/2)(circle(d=cls.breakout_d[0] - 2))) +
                        left(cls.stencil_d[0]/2+6.0)(circle(d=12)) +
                        right(cls.stencil_d[0]/2+6.0)(circle(d=12))))


class soic_8(soic, dil, stencil):
    breakout_d=[9.85, 9.85]
    breakout_t = 1.6
    stencil_offset = [0, soic.E*1.5]
    N = 8

class sot23_6(sot23, dil, stencil):
    N = 6

def export_scad():
    util.save('sot23-6-breakout-stencil', sot23_6.breakout_stencil())
    util.save('sot23-6-breakout-stencil-shim', sot23_6.breakout_stencil_shim())
    util.save('soic-8-breakout-stencil', soic_8.breakout_stencil())
    util.save('soic-8-breakout-stencil-shim', soic_8.breakout_stencil_shim())

if __name__ == '__main__':
    export_scad()
