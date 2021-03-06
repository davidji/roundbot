from solid import *
from solid.utils import *
from util import inch_to_mm
from fixings import NO2
from util import radial

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
        # add a little offset so the fit is comfortable
        return offset(0.1)(hull()(circle(d=metal_3_8.d[1]) +
                                  left(tab_offset)(tab) +
                                  right(tab_offset)(tab)))

    @staticmethod
    def screw_holes():
        return radial(metal_3_8.screw_spacing/2, [-90, 90], NO2.cut())
