from solid import *
from solid.utils import *

import fixings
import util
from util import corners, inch_to_mm, pipe

class board:
    d = inch_to_mm([2.0,0.9]) + [1.6]
    h = inch_to_mm([1.8, 0.7])
    holes = corners(*h)
    fixing = fixings.M2_5

    @staticmethod
    def slot_screw_mount():
        width=board.fixing.nut.f+2.0
        def slot(t=1.0):
            return translate([-width/2, inch_to_mm(-0.1), 0])(
                (cube([width, 2.0*t, 2.0*t+board.d[2]]) -
                 translate([0, t, t])(cube([width, t, board.d[2]]))))

        return up(board.d[1]/2)(rotate([90,0,0])(union()(*(translate(p)(slot()) for p in (board.holes[1], board.holes[2]))) +
                union()(*(
                    translate(p)(down(5.0)(
                        translate([-width/2, -(board.d[1] + board.h[1])/2, 0])(
                            cube([width, board.d[1], 5.0])) +
                        pipe(ir=board.fixing.thread/2.0, t=1.0, h=6.0)) +
                        down(4.0)(rotate([0,0,180])(hole()(board.fixing.nut.side_capture(depth=5.0)))))
                    for p in (board.holes[0], board.holes[3])))))

if __name__ == '__main__':
    util.save('feather-mount', board.slot_screw_mount())
    