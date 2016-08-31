#! /usr/bin/env python
from __future__ import division
import os, sys, re
from math import sqrt

from solid import *
from solid.utils import *
from solid import screw_thread

from pololu.caster import *
from batteries import cr123a
from fixings import M2, M3, NO2
from util import *
from raspberrypi import aplus



FA=0.1
FS=0.5

MOTOR_WIDTH=12.0
CASTER_SPACING=26.0
CR123A_FORWARD=MOTOR_WIDTH/2+1+cr123a.d[1]/2
STANDOFF_HEIGHT=25
BATTERY_OUTSIDE_EDGE=MOTOR_WIDTH/2+1+cr123a.d[1]
CASTER_FORWARD=BATTERY_OUTSIDE_EDGE+2


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
            arch_width=12.0,
            arch_length=35.0,
            caster=metal_3_8,
            min_wall = 2.0,
            tapped=False):


    def m3():
        return M3.cut(tapped)

    def wheel_arch(width=arch_width, length=arch_length):
        return right(radius-width/2)(square([width, length], True))

    # Using the pololu motor mounts is optional. I might also just glue
    # an aluminium angle on the underside to form a bracket for the motor
    # that allows the motor to be flush with the chassis.
    def motor_mount():
        hole = NO2.cut()
        return right(radius-arch_width-4.25)(forward(9)(hole) + back(9)(hole))

    def motor_cutouts():
        right = motor_mount() + wheel_arch();
        left = mirror([1,0,0])(right)
        return left + right

    def motors():
        leftm = color(Steel)(left(radius-arch_width)(back(6)(cube([40.2,12,10], False))))
        rightm = mirror([1,0,0])(leftm)
        return leftm + rightm

        return forward(CR123A_FORWARD)(holes) + back(CR123A_FORWARD)(rotate(180)(holes))

    def cr123a_batteries():
        frontb = color(Green)(up(7)(forward(CR123A_FORWARD)(cube([CR123A_LENGTH,CR123A_WIDTH,CR123A_HEIGHT], True))))
        backb = mirror([0,1,0])(frontb)
        return frontb + backb

    def cr123a_cutout():
        cutout = square([CR123A_LENGTH,CR123A_WIDTH], True)
        return forward(CR123A_FORWARD)(cutout) + back(CR123A_FORWARD)(cutout)

    def caster_mount_screw_holes(tapped=tapped):
        return radial(caster.d[0]/2 + 3, [90, -90], M3.cut(tapped))

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

    def pololu_qtr_3a_holes():
        screw_hole = hole()(m3())
        spacing=inch_to_mm(1.05)
        QTR_3A_FORWARD = CASTER_FORWARD + caster.d[1] + 2 + inch_to_mm(0.3)/2
        return forward(QTR_3A_FORWARD)(
            back(inch_to_mm(0.10))(square([1.1*inch_to_mm(0.4), 1.1*inch_to_mm(0.1)], True)) +
            left(spacing/2)(screw_hole) +
            right(spacing/2)(screw_hole))

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

    def pcb_70x50_mount():
        """This is a generic pcb with M2 corner holes that I have a few of"""
        return corners([46,66], M2.cut())

    def wheels():
        rwheel = up(5)(right(radius-arch_width+5)(rotate([0,90,0])(cylinder(r=16,h=7,center=True))))
        lwheel = mirror([1,0,0])(rwheel)
        return rwheel + lwheel

    def connecting_screw_holes():
        return hole()(radial(radius - 3, [+45, -45, +135, -135], M3.cut()))

    def base():
        return (
            circle(radius) -
            motor_cutouts() -
            caster_holes() -
            connecting_screw_holes() -
            pololu_qtr_3a_holes() -
            radial(CR123A_FORWARD, [0, 180], cr123a.cut_opening()) -
            radial(0, [ 0, 180], 
                   radial(radius-5, [ 30, -30 ], m3()) +
                   radial(radius-10, [30, -30, 45, -45 ], m3())) -
            radial(0, [180],
                   radial(radius-5, [ 15, 0, -15 ], m3())) -
            pen_hole())

    def lid_cut():
        return (circle(radius) -
                aplus.cut_holes() -
                pcb_70x50_mount() -
                radial(0, [0,180], wheel_arch()) -
                connecting_screw_holes() -
                radial(CR123A_FORWARD, [0, 180], cr123a.cut_holes()) -
                radial(35, [90,270], arc(7.5, 180, 0)) -
                radial(35, [0, 180], circle(d=15)))

    def lid():
        return (linear_extrude(height=3)(lid_cut()) -
                rotate_extrude()(translate([-radius, 0])(polygon(([-ABIT,-ABIT],[3,-ABIT],[-ABIT,3])))) +
                radial(radius - 3, [+45, -45, +135, -135], (tube(r=3,ir=1.5,h=3))))

    def body_cross_section(height):
       return translate([radius-1,0])(
            left(2)(square([3,3])) +
            square([1, height]) +
            union()(*(translate([0, y])(polygon([[0,-1],[-1, 0],[0,1]])) 
                      for y in range(1, height, 5))) +
            translate([1, height])(polygon(([0,-3],[-3,0],[0,3]))))

    def body(height=21):
        vstrut = left(1.25)(cube([2.5,2,height]))
        return (rotate_extrude()(body_cross_section(height)) +
                radial(radius - 3, [a + 7.5 for a in range(0,360,15)], vstrut) -
                radial(radius - 3, [+45, -45, +135, -135], up(height)(cylinder(r=3,h=3))))

    def caster_plinth_cut():
        return (square([caster.d[0]+12, caster.d[1]+2*min_wall], True) -
                caster_mount_screw_holes(False) -
                caster.screw_holes())

    def hc_sr04_mount():
        return translate([0, radius, 15])(rotate([90,0,0])(radial(18, [-90,90], pipe(r=10,t=2,h=8))))

    def chassis():
        return (linear_extrude(height=3)(base()) + 
                body() +
                up(3)(radial(radius - 3, [+45, -45, +135, -135], 
                             pipe(r=3, t=1.5, h=cr123a.d[2]))) +
                forward(2*radius+min_wall)(lid()) +
                linear_extrude(height=3)(radial(CR123A_FORWARD, [0, 180], caster_plinth_cut())))

    def extras():
        return (motors() +
            cr123a_batteries() +
            wheels() +
            pololu_caster_mounts() +
            standoffs())

    def plates():
        return (base() + 
                radial(CR123A_FORWARD, [0, 180], caster_plinth_cut()) +
                forward(2*radius+min_wall)(lid()))

    return chassis() # + extras()


def assembly():
    return chassis()
 
if __name__ == '__main__':
    out_dir = sys.argv[1] if len(sys.argv) > 1 else os.curdir
    file_out = os.path.join( out_dir, 'chassis.scad')
 
    a = assembly()
    print("%(__file__)s: SCAD file written to: \n%(file_out)s"%vars())
    scad_render_to_file( a, file_out, file_header='$fa = %s; $fs = %s;' % (FA, FS), include_orig_code=True)
