
from solid import *
from solid.utils import *

class breakout:
    """3mm holes, 8mm back, 9mm apart"""
    d = [13.3,15.9,5.0]
    holes = ([-4.5, -7.5], [4.5, -7.5])

class micro:
    @staticmethod
    def cut():
        return back(7.5/2)(
            translate([0.5, 0.5, 0])(offset(r=0.5)(square([1.5, 6.5]))) + 
            square([1.25, 7.5]))
