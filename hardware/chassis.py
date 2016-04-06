#! /usr/bin/env python
from __future__ import division
import os, sys, re
 
from solid import *
from solid.utils import *
from solid import screw_thread

def inch_to_mm(in_inches):
    try:
        i = iter(in_inches)
    except TypeError:
        return in_inches*25.4
    else:
        return [ inch_to_mm(x) for x in i ]

NO2_SCREW_R=1.1
CASTOR_SPACING=inch_to_mm(0.58)

# Height of platform: the wheels are 16mm, less 3mm for the chassis
# plate, and 5mm half the height of the motor = 8mm
# That's too small for the ball to be mounted on the underside. I can
# have a cutout for the caster, but this will use up lots of space.
# Other alternatives are to mount the motors underneath or in cutouts.
# Underneath means 21mm clearance. That's the size of pololu 1/2" metal
# casters, so I'd better get some of those and keep things simple.
# I could leave the possibility of batteries on the underside open too,
# then a single chassis plate might well be enough.

def chassis(radius=50, arch_width=8, arch_length=35):
    def wheel_arch(width=arch_width, length=arch_length):
        return right(radius-width/2)(square([width, length], True))

    # Using the pololu motor mounts is optional. I might also just glue
    # and aluminium angle on the underside to form a bracket for the motor
    # that allows the motor to be flush with the chassis.
    def motor_mount():
        """https://www.pololu.com/product/989, the screws are 2-56 with diameter 2.184mm"""
        hole = circle(NO2_SCREW_R)
        return right(radius-arch_width-4.25)(forward(9)(hole) + back(9)(hole))

    def motor_cutout():
        return wheel_arch() + motor_mount()

    def motor_cutouts():
        right = wheel_arch() + motor_mount();
        left = mirror([1,0,0])(right)
        return left+right

    def motors():
        leftm = color(Steel)(left(radius-arch_width)(back(6)(cube([40.2,12,10], False))))
        rightm = mirror([1,0,0])(leftm)
        return leftm + rightm

    def batteries():
        frontb = color(Green)(left(53.0/2)(forward(12)(cube([53,24,13], False))))
        backb = mirror([0,1,0])(frontb)
        return frontb + backb
    
    def pololu_castor_mount():
        """See https://www.pololu.com/picture/view/0J474"""
        hole = circle(NO2_SCREW_R)
        castor_r = CASTOR_SPACING/2
        return forward(radius-castor_r)(left(castor_r)(hole) + right(castor_r)(hole))

    def castor_mount():
        """I've bought some miniature 'ball transfer units' on ebay. They
        are push fit. The total diameter is 16mm, and the body diameter is 13mm.
        The total hight is 10mm, so it won't protrude through the hole, but I will
        need to provide 4mm of packing. I have 16mm delrin rod, but need a 13mm
        drill bit for the hole"""
        return forward(radius-10)(circle(6.5))
    
    def castor_mounts():
        front = castor_mount()
        back = mirror([0,1,0])(front)
        return front + back;

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
        rwheel = up(5)(right(radius)(rotate([0,90,0])(cylinder(r=16,h=7,center=True))))
        lwheel = mirror([1,0,0])(rwheel)
        return rwheel + lwheel
    
    return motors() + batteries() + circle(radius) - motor_cutouts() - castor_mounts() - arduino_mount() + wheels()


def assembly():
    return chassis()
 
if __name__ == '__main__':
    out_dir = sys.argv[1] if len(sys.argv) > 1 else os.curdir
    file_out = os.path.join( out_dir, 'chassis.scad')
 
    a = assembly()
    print("%(__file__)s: SCAD file written to: \n%(file_out)s"%vars())
    scad_render_to_file( a, file_out, include_orig_code=True)
