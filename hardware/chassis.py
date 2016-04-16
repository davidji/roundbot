#! /usr/bin/env python
from __future__ import division
import os, sys, re
from math import sqrt

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
M3_TAPPED=1.2
M3=1.5
MOTOR_WIDTH=12
CASTOR_SPACING=inch_to_mm(0.58)
CR123A_WIDTH=18
CR123A_LENGTH=43.2
CR123A_FORWARD=MOTOR_WIDTH/2+1+CR123A_WIDTH/2
POLOLU_CASTOR_R=16/2

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

def chassis(radius=50, arch_width=5, arch_length=35):
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
    def cr123a_battery_holes():
        holes = (
            left(CR123A_LENGTH/2-2.6)(forward(8.2)(circle(0.9))) +
            left(CR123A_LENGTH/2-2.6)(circle(M3, True)) +
            right(CR123A_LENGTH/2-2.6)(circle(M3, True)) +
            left(12.1)(circle(M3_TAPPED, True)) +
            right(12.1)(circle(M3_TAPPED, True)))
        return forward(CR123A_FORWARD)(holes) + back(CR123A_FORWARD)(rotate(180)(holes))
    
    def cr123a_batteries():
        frontb = color(Green)(up(7)(forward(CR123A_FORWARD)(cube([CR123A_LENGTH,CR123A_WIDTH,14], True))))
        backb = mirror([0,1,0])(frontb)
        return frontb + backb

    def nucleo():
        return color(Red)(left(25)(forward(CR123A_FORWARD+CR123A_WIDTH/2+1)(cube([50,18.5,16.5], False))))
    
    def pololu_castor_mount():
        """See https://www.pololu.com/picture/view/0J474"""
        screw_hole = circle(NO2_SCREW_R)
        return forward(radius-POLOLU_CASTOR_R-1)(
            circle(POLOLU_CASTOR_R) +
            left(CASTOR_SPACING/2)(screw_hole) +
            right(CASTOR_SPACING/2)(screw_hole))

    def castor_mount():
        """I've bought some miniature 'ball transfer units' on ebay. They
        are push fit. The total diameter is 16mm, and the body diameter is 13mm.
        The total hight is 10mm, so it won't protrude through the hole, but I will
        need to provide 4mm of packing. I have 16mm delrin rod, but need a 13mm
        drill bit for the hole"""
        return forward((radius-5-6.5))(circle(6.5, True))
    
    def castor_mounts():
        front = pololu_castor_mount()
        left_back = rotate(135)(front)
        right_back = rotate(-135)(front)
        return front + left_back + right_back;

    def pen_hole():
        return circle(5, True)

    def standoff_holes():
        hole = forward(radius - 5)(circle(1.5,True))
        return union()(*(rotate(angle)(hole) for angle in [i*90+45 for i in range(4)]))
    
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
    
    return (motors() +
            cr123a_batteries() +
            circle(radius) -
            motor_cutouts() -
            castor_mounts() -
            standoff_holes() -
            cr123a_battery_holes() -
            pen_hole() +
            wheels() +
            nucleo())


def assembly():
    return chassis()
 
if __name__ == '__main__':
    out_dir = sys.argv[1] if len(sys.argv) > 1 else os.curdir
    file_out = os.path.join( out_dir, 'chassis.scad')
 
    a = assembly()
    print("%(__file__)s: SCAD file written to: \n%(file_out)s"%vars())
    scad_render_to_file( a, file_out, include_orig_code=True)
