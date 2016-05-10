from solid import *
from solid.utils import *
from pololu import *

class metal_3_8:
    d=[inch_to_mm(0.75), inch_to_mm(0.5), inch_to_mm(0.4)]
    screw_spacing=inch_to_mm(0.53)

    @staticmethod
    def outline():
        """Base outline of the caster centred around the origin
        with the screw holes along the x axis - i.e. x is the long axis
        """
        tab = circle(d=(metal_3_8.d[0] - metal_3_8.screw_spacing))
        tab_offset = metal_3_8.screw_spacing/2
        return hull()(circle(d=metal_3_8.d[1]) +
                      left(tab_offset)(tab) +
                      right(tab_offset)(tab))

    @staticmethod
    def screw_holes():
        hole = circle(r=NO2_SCREW_R)
        return left(metal_3_8.screw_spacing/2)(hole) + right(metal_3_8.screw_spacing/2)(hole)
