from solid import *
from solid.utils import *

import fixings
import util
from util import corners,pipe,inch_to_mm, ABIT

class aplus:
    d = [65.0,56.0,10.0]

    @staticmethod
    def cut_holes():
        return corners(58,49)(fixings.M2_5.cut())

class zero:
    d = [65.0, 30.0, 10.0]
    h = [58.0,23.0]
    holes = corners(*h)
    fixing = fixings.M2_5
    
    test = []
    
    @staticmethod
    def outline():
        return hull()(*(translate(p)(circle(r=3.7)) for p in zero.holes))

    @staticmethod
    def shoe(h=2.0):
        gpio_outline = forward(zero.d[1]/2 - 3.5)(square([inch_to_mm(2.0), 7.0], center=True))
        return (
            linear_extrude(h)(zero.outline() - gpio_outline - mirror([0,1,0])(gpio_outline)) +
            linear_extrude(h+2.6)(    
                intersection()(
                    offset(r=1.0)(zero.outline()),
                    union()(*(translate(p)(square([8.0, 8.0], center=True)) for p in zero.holes)))) -
            up(h)(linear_extrude(2.6)(zero.outline())) +
            union()(*(translate(p)(pipe(ir=1.25, r=3.5, h=h+1)) for p in zero.holes)))

    @staticmethod
    def cover(h=1.0, t=2.0):
        return (
            linear_extrude(t+h+1.6)(offset(r=1.0)(zero.outline())) -
            up(t)(linear_extrude(h+1.6+ABIT)(zero.outline())) +
            union()(*(translate(p)(pipe(ir=1.3, r=2.5, h=t+h)) for p in zero.holes)))
    
    @staticmethod
    def wifi_cover():
        holes = corners(34.85, 12.4)[0::2]
        clip = fixings.snapin(d1=2.8, d2=3.6, h1=4.0, h2=2.0, t=1.0)
        offset = zero.d[0]/2 - 20 - 8
        return (zero.cover(t=1.0, h=6.0) +
                right(offset)(union()(*(translate(p)(clip) for p in holes))) +
                hole()(translate([zero.d[0]/2, -7.0, 2.0])(cube([3.0,3.0,7.6]))))

    @staticmethod
    def phat_riser():
        spacing = 11.0

if __name__ == '__main__':
    util.save('raspberrypi-zero-shoe', zero.shoe())
    util.save('raspberrypi-zero-wifi-cover', zero.wifi_cover())
