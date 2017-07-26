#! /usr/bin/env python
from __future__ import division
import os, sys, re
from math import sqrt

from solid import *
from solid.utils import *
from solid import screw_thread

from pololu.caster import *
from batteries import cr123a
from fixings import M2, M2_5, M3, NO2
from util import *
from raspberrypi import aplus
from nucleo import nucleo64
from gearmotor import micrometal

import batteries, raspberrypi
from honeycomb import honeycomb
import feather

from body import body as makebody
from eyes import eyes
import util
from gtk.keysyms import cent
from PIL.GimpGradientFile import linear
from solid.objects import linear_extrude

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

def chassis(body=None,
            arch_width=12.0,
            arch_length=35.0,
            caster=metal_3_8,
            min_wall = 2.0,
            base_thickness=2.0,
            wheel_diameter=34.0,
            insert_height=3.0,
            tapped=False):

    axle_height = base_thickness + micrometal.gearbox_d[2]/2
    arch_id = wheel_diameter + 2.0
    arch_od = arch_id + 2.0*min_wall
    arch_wall_height = axle_height + arch_od/2.0
    pcb_plate_height = battery_holder.d[2]
    pcb_height = arch_wall_height + 2.0

    body = body or makebody(height=arch_wall_height)
    radius = body.radius()
    arch_wall_height = min(body.height(), arch_wall_height)

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

    def qtr_mount(d, screws, sensors):
        return (linear_extrude(base_thickness)(square([x + 2.0 for x in d[0:2]], center=True)) +
                up(1.0)(linear_extrude(d[2])(hole()(
                    difference()(
                        square(d[0:2], center=True),
                        union()(*(translate(p)(circle(r=2.0)) for p in screws)))))) +
                union()(*(translate(p)(pipe(ir=1.0, r=2.0, h=base_thickness + d[2] - 1.0))
                          for p in screws)) +
                union()(*(translate(p)(hole()(linear_extrude(base_thickness)(square([3.0,5.0], center=True))))
                          for p in sensors)) +
                hole()(up(base_thickness + d[2] - 1.0)(linear_extrude(10.0)(square(d[0:2], center=True)))))

    def pololu_qtr_3a_mount():
        d = [32.0, 8.0, 3.0]
        sensors = ([-9.6, 0.0], [0.0, 0.0], [9.6, 0.0])
        screw_spacing=inch_to_mm(1.05)
        QTR_3A_FORWARD = CASTER_FORWARD + caster.d[1] + inch_to_mm(0.3)/2
        return forward(QTR_3A_FORWARD)(
            qtr_mount(d, ([-screw_spacing/2, 0], [screw_spacing/2, 0]), sensors))

    def pololu_qtr_1a_mounts():
        d = [inch_to_mm(0.3), inch_to_mm(0.5), 3.0]
        qtr_1a = qtr_mount(d, [[0, -4.0]], [[0, 1.35]])
        return radial(radius - inch_to_mm(0.5)/2 - 2.0, [+30, -30], qtr_1a)

    def neopixels():
        return radial(radius-4, [ -150, 150, -165, 165, -180 ],
            up(body.height()/2)(rotate([-90,0,0])(
                hole()(
                    cylinder(d=5.0,h=5.0) + 
                    linear_extrude(3.0)(square([5.5, 5.5], center=True))) +
                cylinder(d=12, h=5.0) +
                translate([-6, 0])(cube([12,body.height()/2, 5.0])) -
                linear_extrude(2.2)(
                    intersection()(
                        circle(d=10.5), 
                        square([11.0,8.5], center=True))))))

    def wheels():
        rwheel = up(5)(right(radius-arch_width+5)(rotate([0,90,0])(cylinder(r=16,h=7,center=True))))
        lwheel = mirror([1,0,0])(rwheel)
        return rwheel + lwheel

    def base():
        return (intersection()(
            (circle(radius-3) -
             radial(0, [0,180], wheel_arch())),
             honeycomb(1.5, 1.0, 100.0, 100.0, center=True) +
             square([2*radius, 2*CR123A_FORWARD + battery_holder.d[0]], center=True) -
             pen_hole()))

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

    def insert_pillar(height=pcb_height, fixing=M2, insert_height=3.0):
        return (tube(h=height, ir=fixing.thread/2.0, r=fixing.insert/2.0+1.0) +
                  up(height-insert_height)(hole()(cylinder(d=fixing.insert, h=insert_height))))

    def nucleo64_pillars():
        return union()(*(translate(p)(insert_pillar(fixing=M2)) for p in nucleo64.holes))

    def pcb_50x70_pillars():
        return union()(*(translate(p)(insert_pillar(fixing=M2)) for p in corners(46,66)))

    def raspberry_pi_zero_pillars():
        return back(radius - arch_width - raspberrypi.zero.d[1]/2)(
                union()(*(translate(p)(insert_pillar(fixing=M2)) for p in raspberrypi.zero.holes)))

    def pcb_plate_fixings(fixing):
        return union()(*(
            translate(p)(fixing) 
            for p in corners(2*(radius - arch_width - min_wall - M2.thread), 2*CR123A_FORWARD) +
            corners(25,50)))

    def pcb_support_pillars():
        return pcb_plate_fixings(insert_pillar(pcb_plate_height, fixing=M2))

    def pcb_plate_rim():
        def triangle(d):
            return polygon(([0, 0], [-d, 0], [0, -d]))
        side = right(radius - arch_width - min_wall)(
                rotate([90,0,0])(linear_extrude(2*radius, center=True)(
                    triangle(min_wall))))
        return up(pcb_plate_height)(
            side + mirror([1,0,0])(side))

    def battery_holders():
        return rotate([0,0,-90])(battery_holder.back() + battery_holder.screw_cover_mount())

    def caster_holder():
        return (linear_extrude(height=base_thickness*2+M2.nut.h)(offset(r=2)(caster.outline())) +
                hole()(linear_extrude(height=base_thickness)(caster.outline())) +
                hole()(up(base_thickness)(linear_extrude(height=base_thickness)(caster.screw_holes()))) +
                hole()(up(base_thickness*2)(
                    radial(caster.screw_spacing/2, [-90, 90], 
                           M2.nut.capture(h=4.0)))))

    def casters():
        return radial(CASTER_FORWARD + caster.d[1]/2, [0,180], caster_holder())

    def hc_sr04_mount():
        return translate([0, radius, 15])(rotate([90,0,0])(radial(18, [-90,90], pipe(r=10,t=2,h=8))))

    def motor_positions(a):
        return radial(radius-arch_width, [90, -90], rotate([0, 0, 180])(a))

    def motors_mounts():
        return motor_positions(micrometal.shoe())

    def motors_cover_voids():
        return motor_positions(micrometal.motor_cover_void())

    def motors_screw_holes():
        return motor_positions(hole()(micrometal.cover_screws(base_thickness)))

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

    def wheel_arches():
        return radial(radius - arch_width, [90, -90], 
                      up(axle_height)(
                          rotate([-90, 0, 0])(
                              linear_extrude(height=arch_width)(
                                  circle(d=arch_od) + 
                                  hole()(circle(d=arch_id))))))

    def reinforcement():
        wheel_wall = up(arch_wall_height/2)(cube([min_wall, 2*radius, arch_wall_height], center=True))
        battery_wall = up(battery_holder.d[2]/2)(
            cube([min_wall, 2*(CR123A_FORWARD), battery_holder.d[2]], center=True))
        cross_wall_h=micrometal.shoe_d()[2]+base_thickness
        cross_wall = up(cross_wall_h/2)(
            cube([2*(radius-arch_width), min_wall, cross_wall_h], center=True) -
            cube([10, min_wall, battery_holder.d[2]], center=True))

        castor_brace=translate([0,CR123A_FORWARD,battery_holder.d[2]/2])(rotate([-50.0, 0, 0])(
            forward(7.5)(cube([min_wall, 15.0, battery_holder.d[2]], center=True))))
        castor_braces=left(10.0)(castor_brace) + right(10.0)(castor_brace)

        return intersection()(
            union()(
                left(radius - arch_width - min_wall/2.0)(wheel_wall),
                right(radius - arch_width - min_wall/2.0)(wheel_wall),
                castor_braces,
                mirror([0,1,0])(castor_braces),
                left(6.0)(battery_wall),
                right(6.0)(battery_wall),
                forward(7.0+min_wall/2)(cross_wall),
                back(7.0+min_wall/2)(cross_wall)),
            up(base_thickness)(cylinder(r=radius-1, h=body.height()-base_thickness)))


    def frontmost(d, r=radius - 3.0):
        y = sqrt(pow(r, 2.0)-pow(d[0]/2, 2.0)) - d[1]/2
        return translate([0,y,0])           
            
    def feather_mount():
        base_height = base_thickness*2+M2.nut.h-2.0
        return rotate([0,0,180])(frontmost([feather.board.d[0], 10.0], r=radius)(
                    up(base_height)(
                        feather.board.slot_screw_mount()) +
                    linear_extrude(base_height)(
                        square([feather.board.d[0] + 2.0, 30.0], center=True) -
                        square([feather.board.d[0] - 12.0, 30.0], center=True))))

    def headlights():
        block = forward(6.0)(linear_extrude(body.height())(square([8,12], center=True)))
        return frontmost([70.0,0])(
            union()(*(translate([x, 0.0, body.height()/2 + z])(
                rotate([-90, 0, 0])(
                    pipe(ir=2.5, r=4.0, h=4.0) +
                    up(4.0)(cylinder(d1=8.0, d2=13.0, h=8.0) + 
                            hole()(cylinder(d1=5.0, d2=13.0, h=8.0)))))
                for (x,z) in corners(65, 12))) +
                left(65.0/2)(block) + right(65.0/2)(block))

    class Chassis:
        def radius(self):
            return radius
        
        def _base_sensors(self):
            return (pololu_qtr_3a_mount() +
                    pololu_qtr_1a_mounts())
        
        def _no_base_sensors(self):
            return (
                battery_holders() +
                reinforcement() +
                casters() +
                wheel_arches() +
                motors_mounts() +
                motor_connector_slots() +
                headlights() +
                pcb_support_pillars() +
                neopixels())

        def chassis(self):
            return intersection()(
                cylinder(r=radius, h=body.height()),
                linear_extrude(height=base_thickness)(base()) +
                self._no_base_sensors() +
                self._base_sensors() + body.body())

        def _base_connectors(self):
            def connector(height):
                return (pipe(r=3.0, ir=1.1, h=height) +
                        up(height-M2.nut.h)(hole()(rotate([0,0,90])(M2.nut.capture(h=M2.nut.h*2)))))

            return (radial(radius-5.0, [+37.5, -37.5], connector(12.0)) +
                    radial(radius-5.0, [+142.5, -142.5], connector(8.0)))

        def base(self):
            return (intersection()(
                    cylinder(r=radius, h=base_thickness),
                    linear_extrude(height=base_thickness)(base()) +
                    self._no_base_sensors() +
                    self._base_connectors() + 
                    motors_screw_holes() +
                    body.body()) + self._base_sensors())

        def upper(self):
            return intersection()(
                up(base_thickness)(cylinder(r=radius, h = body.height() - base_thickness)),
                self._no_base_sensors() +
                self._base_sensors() +
                self._base_connectors() +
                body.body())

        def fullbody(self):
            return (self.chassis() + body.body())

        def modularbody(self):
            return ((self.chassis() - body.end_modules_bounds())  + body.sides())

        def extras(self):
            return (motors() +
                cr123a_batteries() +
                wheels() +
                pololu_caster_mounts() +
                standoffs())

        def pcb_plate_blank(self):
            width = 2.0*(radius - arch_width - min_wall)
            return linear_extrude(min_wall)(
                intersection()(
                    circle(r=radius-3.0), 
                    square([width, 2*radius], center=True)) +
                pcb_plate_fixings(hole()(M2.cut())))
    
        def pcb_plate(self):
            width = 2.0*(radius - arch_width - min_wall)
            
            return (self.pcb_plate_blank() +
                    mirror([0,1,0])(frontmost([70,50])(union()(
                        *(translate(p)(insert_pillar(height=3.0, fixing=M2)) 
                          for p in corners(66,46))))) +
                    frontmost(raspberrypi.zero.d)(union()(
                        *(translate(p)(insert_pillar(height=3.0, fixing=M2_5)) 
                          for p in raspberrypi.zero.holes))))

        def plates(self):
            return (base() + 
                    radial(CR123A_FORWARD, [0, 180], caster_plinth_cut()) +
                    forward(2*radius+min_wall)(lid()))

    return Chassis() # + extras()



def export_scad():
    util.save('chassis', chassis().fullbody())
    util.save('chassis-base', chassis().base())
    util.save('chassis-upper', chassis().upper())
    util.save('chassis-pcb-plate', chassis().pcb_plate())
    util.save('chassis-modular', chassis().modularbody())
    util.save('chassis-battery-cover', battery_holder.screw_cover())

if __name__ == '__main__':
    export_scad()
