#! /usr/bin/env python
from __future__ import division
import os, sys, re
from math import sqrt

from solid import *
from solid.utils import *
from solid import screw_thread

from pololu.caster import *


ABIT=0.1
FA=0.1
FS=0.5

M3_TAPPED=1.25
M3=1.5
MOTOR_WIDTH=12.0
CASTER_SPACING=26.0
CR123A_WIDTH=18.0
CR123A_LENGTH=43.2
CR123A_HEIGHT=18.0
CR123A_FORWARD=MOTOR_WIDTH/2+1+CR123A_WIDTH/2
STANDOFF_HEIGHT=25
BATTERY_OUTSIDE_EDGE=MOTOR_WIDTH/2+1+CR123A_WIDTH
CASTER_FORWARD=BATTERY_OUTSIDE_EDGE+2

def cr123a_battery_holes(tapped=False):
    return (
        left(CR123A_LENGTH/2-2.6)(forward(8.2)(circle(0.9))) +
        left(CR123A_LENGTH/2-2.6)(circle(M3, True)) +
        right(CR123A_LENGTH/2-2.6)(circle(M3, True)) +
        left(12.1)(circle(tapped and M3_TAPPED or M3, True)) +
        right(12.1)(circle(tapped and M3_TAPPED or M3, True)))

def corners(d, o=None):
    return ([p*d for p in v]  for v in CORNERS)


# Height of platform: the wheels are 16mm, less 3mm for the chassis
# plate, and 5mm half the height of the motor = 8mm
# That's too small for the ball to be mounted on the underside. I can
# have a cutout for the caster, but this will use up lots of space.
# Other alternatives are to mount the motors underneath or in cutouts.
# Underneath means 21mm clearance. That's the size of pololu 1/2" metal
# casters, so I'd better get some of those and keep things simple.
# I could leave the possibility of batteries on the underside open too,
# then a single chassis plate might well be enough.

def chassis(radius=50.0,
            arch_width=10.0,
            arch_length=35.0,
            caster=metal_3_8,
            min_wall = 2.0,
            tapped=False):

    def m3():
        return circle(tapped and M3_TAPPED or M3, True)

    def wheel_arch(width=arch_width, length=arch_length):
        return right(radius-width/2)(square([width, length], True))

    # Using the pololu motor mounts is optional. I might also just glue
    # an aluminium angle on the underside to form a bracket for the motor
    # that allows the motor to be flush with the chassis.
    def motor_mount():
        """https://www.pololu.com/product/989, the screws are 2-56 with diameter 2.184mm"""
        hole = circle(NO2_SCREW_R)
        return right(radius-arch_width-4.25)(forward(9)(hole) + back(9)(hole))

    def motor_cutouts():
        right = motor_mount() + wheel_arch();
        left = mirror([1,0,0])(right)
        return left + right

    def motors():
        leftm = color(Steel)(left(radius-arch_width)(back(6)(cube([40.2,12,10], False))))
        rightm = mirror([1,0,0])(leftm)
        return leftm + rightm

    # this is a specific CR123A battery holder from Spiratronics
    # This is intended to be PCB mount. I'm just going to solder wires onto
    # the tables, wrap them in shrinkwrap, and they will go though holes in
    # the chassis. The index hole is mean to be M1.8. No doubt a 2mm hole will do
    # From the Spiratronics provided datasheet:
    # http://www.spiratronics.com/data/3785.pdf
        return forward(CR123A_FORWARD)(holes) + back(CR123A_FORWARD)(rotate(180)(holes))

    def cr123a_batteries():
        frontb = color(Green)(up(7)(forward(CR123A_FORWARD)(cube([CR123A_LENGTH,CR123A_WIDTH,CR123A_HEIGHT], True))))
        backb = mirror([0,1,0])(frontb)
        return frontb + backb

    def cr123a_cutout():
        cutout = square([CR123A_LENGTH,CR123A_WIDTH], True)
        return forward(CR123A_FORWARD)(cutout) + back(CR123A_FORWARD)(cutout)

    def nucleo():
        return color(Red)(left(25)(forward(CR123A_FORWARD+CR123A_WIDTH/2+1)(cube([50,18.5,16.5], False))))

    def caster_mount_screw_holes():
        screw_hole = m3()
        screw_offset = caster.d[0]/2 + 3
        return (left(screw_offset)(screw_hole) +
                right(screw_offset)(screw_hole))

    def pololu_caster_holes():
        return (
            caster.outline() +
            caster_mount_screw_holes())

    def caster_hole():
        """I've bought some miniature 'ball transfer units' on ebay. They
        are push fit. The total diameter is 16mm, and the body diameter is 13mm.
        The total height is 10mm, so it won't protrude through the hole, but I will
        need to provide 4mm of packing. I have 16mm delrin rod, but need a 13mm
        drill bit for the hole"""
        return forward((radius-5-6.5))(circle(6.5, True))

    def for_each_caster(x):
        return union()(*(rotate(a)(forward(CASTER_FORWARD + caster.d[1]/2)(x)) for a in (0, 180)))

    def caster_holes():
        return for_each_caster(pololu_caster_holes())

    def pololu_caster_mount():
        return up(1.5+1+2)(
            square([CASTER_SPACING+8,8], True) -
            caster_mount_screw_holes())

    def pololu_caster_mounts():
        return for_each_caster(pololu_caster_mount())

    def pen_hole():
        return circle(5, True)

    def for_each_standoff(x):
        return union()(*(rotate(angle)(forward(radius - 3)(x)) for angle in (+45, -45, +135, -135)))

    def standoff_holes():
        return for_each_standoff(circle(M3))

    def pololu_qtr_3a_holes():
        hole = m3()
        spacing=inch_to_mm(1.05)
        QTR_3A_FORWARD = CASTER_FORWARD + caster.d[1] + 2 + inch_to_mm(0.3)/2
        return forward(QTR_3A_FORWARD)(
            back(inch_to_mm(0.10))(square([1.1*inch_to_mm(0.4), 1.1*inch_to_mm(0.1)], True)) +
            left(spacing/2)(hole) +
            right(spacing/2)(hole))

    def standoffs():
        return for_each_standoff(cylinder(r=3,h=STANDOFF_HEIGHT))

    def arduino_mount():
        """The plan is to use a nucleo board, which has arduino mounting screw points"""
        # coordinates are in inches as per arduino spec, converted in loop
        holes = union()(*(translate(inch_to_mm(coordinates))(circle(1.5))
                         for coordinates in (
                               [0.0 ,0.0 ,0.0],
                               [1.9 ,0.05,0.0],
                               [1.3 ,2.05,0.0],
                               [0.2 ,2.05,0.0])))
        # The nucleo board is ~82.5mm accross
        return back(inch_to_mm(2.05)-12)(left(inch_to_mm(1.9/2))(holes))

    def wheels():
        rwheel = up(5)(right(radius-arch_width+5)(rotate([0,90,0])(cylinder(r=16,h=7,center=True))))
        lwheel = mirror([1,0,0])(rwheel)
        return rwheel + lwheel

    def outline():
        return (
            circle(radius) -
            motor_cutouts() -
            caster_holes() -
            standoff_holes() -
            pololu_qtr_3a_holes() -
            # cr123a_battery_holes() -
            cr123a_cutout() -
            pen_hole())

    def chassis():
        return linear_extrude(height=3)(outline())

    def extras():
        return (motors() +
            cr123a_batteries() +
             +
            wheels() +
            pololu_caster_mounts() +
            standoffs())

    return chassis() # + extras()


def assembly():
    return chassis()
 
if __name__ == '__main__':
    out_dir = sys.argv[1] if len(sys.argv) > 1 else os.curdir
    file_out = os.path.join( out_dir, 'chassis.scad')
 
    a = assembly()
    print("%(__file__)s: SCAD file written to: \n%(file_out)s"%vars())
    scad_render_to_file( a, file_out, file_header='$fa = %s; $fs = %s;' % (FA, FS), include_orig_code=True)
