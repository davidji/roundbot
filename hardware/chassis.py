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
from nucleo import nucleo64
from gearmotor import micrometal

import batteries
from honeycomb import honeycomb

from body import body
from eyes import eyes
import util

CELL_DIAMETER = 17.0
CELL_LENGTH = 34.5
MOTOR_WIDTH=12.0
CASTER_SPACING=26.0
CR123A_FORWARD=MOTOR_WIDTH/2+CELL_DIAMETER/2+2.0
STANDOFF_HEIGHT=25
BATTERY_OUTSIDE_EDGE=MOTOR_WIDTH/2+2+CELL_DIAMETER
CASTER_FORWARD=BATTERY_OUTSIDE_EDGE

battery_holder = batteries.PanelHolder(
    cell_length=CELL_LENGTH,
    cell_diameter=CELL_DIAMETER,
    cell_offsets = [ -CR123A_FORWARD, +CR123A_FORWARD])



# Height of platform: the wheels are 16mm, less 3mm for the chassis
# plate, and 5mm half the height of the motor = 8mm
# That's too small for the ball to be mounted on the underside. I can
# have a cutout for the caster, but this will use up lots of space.
# Other alternatives are to mount the motors underneath or in cutouts.
# Underneath means 21mm clearance. That's the size of pololu 1/2" metal
# casters, so I'd better get some of those and keep things simple.
# I could leave the possibility of batteries on the underside open too,
# then a single chassis plate might well be enough.

def chassis(body=eyes().body(),
            arch_width=12.0,
            arch_length=35.0,
            caster=metal_3_8,
            min_wall = 2.0,
            base_thickness=2.0,
            tapped=False):

    radius = body.radius()

    def m3():
        return M3.cut(tapped)

    def wheel_arch(width=arch_width, length=2*radius):
        return right(radius-width/2)(square([width, length], True))

    def motors():
        leftm = color(Steel)(left(radius-arch_width)(back(6)(cube([40.2,12,10], False))))
        rightm = mirror([1,0,0])(leftm)
        return leftm + rightm

        return forward(CR123A_FORWARD)(holes) + back(CR123A_FORWARD)(rotate(180)(holes))

    def cr123a_batteries():
        frontb = color(Green)(up(7)(forward(CR123A_FORWARD)(cube([CR123A_LENGTH,CR123A_WIDTH,CR123A_HEIGHT], True))))
        backb = mirror([0,1,0])(frontb)
        return frontb + backb

    def pen_hole():
        return circle(5, True)

    def pololu_qtr_3a_mount():
        screw_mount = (pipe(ir=1.0, t=min_wall, h=base_thickness+2.0) + 
                       hole()(up(base_thickness)(M2.nut.capture(2.0))))
        spacing=inch_to_mm(1.05)
        cable_outline = square([1.1*inch_to_mm(0.5), 1.1*inch_to_mm(0.1)], True)
        cable_slot = linear_extrude(height=base_thickness)(
            offset(min_wall)(cable_outline) + hole()(cable_outline))
        QTR_3A_FORWARD = CASTER_FORWARD + caster.d[1] + inch_to_mm(0.3)/2
        return forward(QTR_3A_FORWARD)(
            rotate([0,0,180])(
                back(inch_to_mm(0.10))(cable_slot) +
                left(spacing/2)(screw_mount) +
                right(spacing/2)(screw_mount)))

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
        return (intersection()(
            (circle(radius-3) -
             radial(0, [0,180], wheel_arch()) -
             connecting_screw_holes()),
            honeycomb(1.5, 1.0, 100.0, 100.0, center=True)) +
            square([2*(radius-arch_width), 2*CR123A_FORWARD + battery_holder.d[0]], center=True) -
            pen_hole())

    def lid_cut():
        return (circle(radius) -
                aplus.cut_holes() -
                pcb_70x50_mount() -
                rotate(90)(pcb_70x50_mount()) -
                nucleo64.cut_holes() -
                radial(0, [0,180], wheel_arch()) -
                connecting_screw_holes() -
                radial(35, [90,270], arc(7.5, 180, 0)) -
                radial(35, [0, 180], circle(d=15)))

    def lid():
        return (linear_extrude(height=3)(lid_cut()) -
                rotate_extrude()(translate([-radius, 0])(polygon(([0,0],[3,0],[0,3])))) +
                radial(radius - 3, [+45, -45, +135, -135], (tube(r=3,ir=1.5,h=3))))

    def nucleo64_pillars(insert_height=3.0):
        height=battery_holder.d[2] + 2
        pillar = tube(h=height, ir=1.5, t=1.5) + up(height-insert_height)(hole()(cylinder(d=M3.insert, h=insert_height)))
        return union()(*(translate(p)(pillar) for p in nucleo64.holes))

    def battery_holders():
        return rotate([0,0,90])(battery_holder.back() + battery_holder.screw_cover_mount())

    def caster_holder():
        return (linear_extrude(height=base_thickness*2+NO2.nut.h)(offset(r=2)(caster.outline())) +
                hole()(linear_extrude(height=base_thickness)(caster.outline())) +
                hole()(up(base_thickness)(linear_extrude(height=base_thickness)(caster.screw_holes()))) +
                hole()(up(base_thickness*2)(
                    radial(caster.screw_spacing/2, [-90, 90], 
                           NO2.nut.capture(h=4.0)))))

    def casters():
        return radial(CASTER_FORWARD + caster.d[1]/2, [0,180], caster_holder())

    def hc_sr04_mount():
        return translate([0, radius, 15])(rotate([90,0,0])(radial(18, [-90,90], pipe(r=10,t=2,h=8))))

    def motors_mounts():
        return radial(radius-arch_width, [90, -90], rotate([0, 0, 180])(micrometal.shoe()))

    def motor_connector_slots():
        """The motors have an jst-ph connector on top of them. It's 14x8x5mm
        and 17mm from the end. I have to be able to slide it all the way through
        from the bottom, because I can't attach the wheel any other way"""
        return radial(radius - arch_width - 17, [90, -90], hole()(
            back(9)(left(7)(cube([14, 10, base_thickness+micrometal.gearbox_d[2]+5]))) +
            translate([-7,-14,base_thickness+micrometal.gearbox_d[2]])(cube([14, 20, 5]))))

    def recycling(resin=1):
        t=unichr(0x2672 + resin)
        t='a'
        return translate([radius-arch_width,CR123A_FORWARD, 0])(
            hole()(linear_extrude(1.0)(text(t))))

    def wheel_archs():
        wheel_diameter=34
        return intersection()(
            cylinder(r=radius, h=body.height()),
            radial(radius - arch_width, [90, -90], 
                      up(base_thickness + micrometal.gearbox_d[2]/2)(
                          rotate([-90, 0, 0])(
                              linear_extrude(height=arch_width)(
                                  circle(d=wheel_diameter+2*min_wall) + 
                                  hole()(circle(d=wheel_diameter)))))))

    def reinforcement():
        wheel_wall = up(body.height()/2)(cube([min_wall, 2*radius, body.height()], center=True))
        battery_wall = up(battery_holder.d[2]/2)(
            cube([min_wall, 2*(CR123A_FORWARD), battery_holder.d[2]], center=True))
        cross_wall_h=micrometal.shoe_d()[2]+base_thickness
        cross_wall = up(cross_wall_h/2)(
            cube([2*(radius-arch_width), min_wall, cross_wall_h], center=True) -
            cube([10, min_wall, battery_holder.d[2]], center=True))

        return intersection()(
            union()(
                left(radius - arch_width - min_wall/2.0)(wheel_wall),
                right(radius - arch_width - min_wall/2.0)(wheel_wall),
                left(6.0)(battery_wall),
                right(6.0)(battery_wall),
                forward(7.0+min_wall/2)(cross_wall),
                back(7.0+min_wall/2)(cross_wall)),
            up(base_thickness)(cylinder(r=radius-1, h=body.height()-base_thickness)))

    class Chassis:
        def chassis(self):
            return (linear_extrude(height=base_thickness)(base()) +
                    battery_holders() +
                    reinforcement() +
                    casters() +
                    wheel_archs() +
                    motors_mounts() +
                    motor_connector_slots() +
                    nucleo64_pillars() +
                    pololu_qtr_3a_mount())

        def fullbody(self):
            return (self.chassis() + body.body())

        def modularbody(self):
            return ((self.chassis() - body.end_modules_bounds())  + body.sides())

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

    return Chassis() # + extras()

def export_scad():
    util.save('chassis', chassis().fullbody())
    util.save('chassis-modular', chassis().modularbody())
    util.save('chassis-battery-cover', battery_holder.screw_cover())

if __name__ == '__main__':
    export_scad()
