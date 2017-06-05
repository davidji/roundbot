
from solid import *
from solid.utils import *
import util
from util import ABIT
from fixings import M3, M2_5

FIXING=M3

class micrometal:
    gearbox_d = [ 12.1, 15.0, 10.0 ] # W D H

    @staticmethod
    def motor_profile(center=False):
        centered = intersection()(circle(d=12), square([12, 10], center=True))
        return center and centered or translate([6, 5, 0])(centered)

    @staticmethod
    def cover(wall_thickness=2.0):
        return (linear_extrude(height=wall_thickness)(
            micrometal.cover_profile(wall_thickness)) +
            hole()(micrometal.cover_screws(wall_thickness)))

    @staticmethod
    def cover_screws(wall_thickness):
        w = micrometal.gearbox_d[0]
        d = micrometal.gearbox_d[1]
        r = d/2
        x = w/2 + wall_thickness + FIXING.nut.f/2
        nut = up(wall_thickness*2)(FIXING.nut.capture(h=6.0-wall_thickness+ABIT))
        screw = down(ABIT)(linear_extrude(height=6.0+2*ABIT)(FIXING.cut())) + nut
        return forward(r)(left(x)(screw) + right(x)(screw))

    @staticmethod
    def cover_void(wall_thickness):
        id = micrometal.gearbox_d
        return hole()(
            micrometal.cover_screws(wall_thickness) +
            down(ABIT)(
                linear_extrude(height=wall_thickness+ABIT)(
                    offset(0.1)(micrometal.cover_profile(wall_thickness)))),
            translate([-id[0]/2, 0, -id[2]+wall_thickness])(cube([id[0], id[1]+22.0, id[2]])))

    @staticmethod
    def cover_profile(wall_thickness=2.0):
        w = micrometal.gearbox_d[0]
        d = micrometal.gearbox_d[1]
        r = d/2
        x = w/2 + wall_thickness + FIXING.nut.f/2
        end = forward(r)(circle(d=d))
        return (hull()(left(x)(end), right(x)(end)) +
                (left(w/2)(square([w, d+1.0]))))

    @staticmethod
    def body_d(wall_thickness=2.0):
        id = micrometal.gearbox_d
        return [id[0] + 2*wall_thickness,
                id[1] + 1.0,
                id[2] + wall_thickness]

    @staticmethod
    def shoe_d(wall_thickness = 2.0):
        id = micrometal.gearbox_d
        return [id[0] + 2 * wall_thickness, id[1] + 1.0, 
            id[2] + wall_thickness]

    @staticmethod
    def shoe(wall_thickness=2.0):
        id = micrometal.gearbox_d
        od = micrometal.shoe_d(wall_thickness)
        clip_radius = 2.2
        motor_length = 18.0

        def gearbox_void():
            divider_thickness=0.825
            divider=right(wall_thickness)(cube([id[0], divider_thickness, id[2]]))
            return (
                translate([wall_thickness, 1.0, 0])(
                    forward(ABIT)(cube([id[0], id[1]+2*ABIT, id[2]])) -
                    up(id[2] - clip_radius)(
                        cube([clip_radius, id[1], clip_radius]) -
                        right(clip_radius)(rotate([-90, 0, 0])(cylinder(h=id[1], r=clip_radius))))) +
                forward(1.0)(divider) +
                forward(4.0 + 1.0 - divider_thickness)(divider) +
                forward(9.0 + 1.0 - divider_thickness)(divider))

        def motor_void():
            return translate([wall_thickness, 1.0 + ABIT, 0])(
                    rotate([90, 0, 0])(
                        linear_extrude(1.0 + ABIT)(
                            micrometal.motor_profile() +
                            square([id[0], id[2]/2]))))

        def base():
            tab_width=wall_thickness + FIXING.thread/2 + micrometal.gearbox_d[1]/2
            return translate([-tab_width, 0, -wall_thickness])(
                cube([od[0]+2*tab_width, od[1], wall_thickness*2+3]))


        return (rotate([0,0,180])(
            translate([-od[0]/2, -od[1], wall_thickness])(
                base() +
                cube(od) +
                hole()(gearbox_void()) +
                hole()(motor_void()))) +
            micrometal.cover_void(wall_thickness))

if __name__ == '__main__':
    util.save('micrometal-shoe', micrometal.shoe())
    util.save('micrometal-cover', micrometal.cover())
