from __future__ import division
import os, sys, re
from math import sqrt

from solid import *
from solid.utils import *
from solid import screw_thread

from chassis import *

def tube(r, h, ir = None, t = None, center=False, hole=False):
    return (cylinder(r=r, h=h, center=center) -
            down(ABIT)(cylinder(r=(t and r - t or ir), h=h+2*ABIT)))

def base_cube(d):
    return up(d[2]/2)(cube(d, True))

def base_open_box(d, t):
    return (base_cube([d[0] + 2*t, d[1] + 2*t, d[2]+t]) - hole()(base_cube(d)))

def chassis(
    radius=45.0, 
    height=20.0, 
    arch_width=5.0, 
    arch_length=35.0,
    caster_d=10.0,
    min_wall=2.0,
    base_thickness=2.0,
    brace_thickness=2.0,
    wheel_r=16,
    wheel_w=8):

    ground_clearance = wheel_r - base_thickness - 5
    battery_box_height = CR123A_HEIGHT+min_wall
    battery_box_width = CR123A_WIDTH+2*min_wall
    battery_box_length = CR123A_LENGTH+2*min_wall

    print "ground clearance: {}".format(ground_clearance)

    def brace(x, y):
        return down(brace_thickness/2)(
            linear_extrude(height=brace_thickness)(
                    translate([x,y,0])(mirror([0,1,0])(mirror([1,0,0])(square([x,y]) - scale([x, y])(circle(r=1)))))))

    def vbrace(l, h):
        return rotate([0, -90, 0])(brace(h, l))

    def perimeter():
        def rib(angle):
            return rotate([0,0,angle])(forward(radius - min_wall/2)(cylinder(d=min_wall, h=height)))

        def ribs(step=5):
            return union()(*(rib(x*step) for x in range(int(360/step))))

        return (ribs() + tube(r=radius, t = 1, h=height))

    def casters(x):
        x2 = forward(radius - caster_d)(x)
        return x2 + rotate([0, 0, 180])(x2)

    def batteries(x):
        return forward(CR123A_FORWARD)(x) + back(CR123A_FORWARD)(x)

    def base(center_r=8):
        def spoke(angle):
            return up(1)(rotate([0,90,angle])(up(center_r)(cylinder(d=min_wall, h=radius-1-center_r))))
        def spokes(step=5):
            return union()(*(spoke(x*step) for x in range(int(360/step))))

        return (cylinder(r=radius, h=1) + 
                spokes() + 
                cylinder(r=center_r, h=min_wall) +
                tube(r=radius, t=min_wall*2, h=min_wall))

    def caster(inset=0.2, clearance=8):
        rb=caster_d/2
        hi = inset*rb
        hb = max(min_wall, caster_d*0.2)
        ri = sqrt(1 - (1 - inset)**2)*rb
        return down(clearance - rb)(cylinder(r = rb + min_wall, h = rb + hb) -
                hole()(down(ABIT)(cylinder(r=rb*1.01, h=rb+ABIT)) +
                 up(rb-ABIT)(cylinder(r=ri, h=hb+2*ABIT))))

    def pololu_3_8_caster_mount():
        screw_offset = inch_to_mm(0.53/2)

        inset = inch_to_mm(0.4) + 2 - ground_clearance
        screw_hole = up(inset - ABIT)(cylinder(r=NO2_SCREW_R, h=base_thickness+2*ABIT))
        x_width = inch_to_mm(0.75) + 2*min_wall
        x_half_length = inch_to_mm(0.25) + min_wall
        x_height = inset + min_wall
        base = translate([0, -x_half_length/2, base_thickness/2])(cube([x_width, x_half_length, base_thickness], True))
        brace = translate([0, -x_half_length, base_thickness])(vbrace(x_half_length, battery_box_height - base_thickness))
        brace_offset = (x_width - brace_thickness)/2
        cup = linear_extrude(height = x_height)(offset(min_wall)(outline()))

        return (cup + left(brace_offset)(brace) + right(brace_offset)(brace) + base -
                hole()(down(ABIT)(linear_extrude(height=inset+ABIT)(outline())) +
                       left(screw_offset)(screw_hole) +
                       right(screw_offset)(screw_hole)))

    def pololu_motor_mount():
        screw_hole = hole()(down(ABIT)(cylinder(r=NO2_SCREW_R, h=base_thickness+2*ABIT)))
        screw_offet = 9
        width = 18 + 8.5 + 2*brace_thickness
        brace_offset = (width - brace_thickness)/2;
        brace = up(base_thickness)(back(11.5/2)(vbrace(11.5, battery_box_height - base_thickness)))
        return back(11.5/2)(
                    left(brace_offset)(brace) +
                    right(brace_offset)(brace) +
                    base_cube([width, 11.5, base_thickness]) -
                    left(screw_offet)(screw_hole) -
                    right(screw_offet)(screw_hole))

    def push_fit_caster():
        tube(r=16, ir=13,h=6)

    def battery_plinth():
        return up(CR123A_HEIGHT + base_thickness/2)(cube([CR123A_LENGTH, CR123A_WIDTH, base_thickness], True))

    def battery_box():
        x_length=battery_box_length
        x_width=battery_box_width
        x_height=battery_box_height
        fixing_screw = up(CR123A_HEIGHT-ABIT)(cylinder(r=M3,h=min_wall+2*ABIT))
        fixing_screw_offset = 12.1
        screws = (left(fixing_screw_offset)(fixing_screw) +
                  right(fixing_screw_offset)(fixing_screw))
        internal = (up(CR123A_HEIGHT/2-ABIT)(cube([CR123A_LENGTH, CR123A_WIDTH, CR123A_HEIGHT+ABIT], True)))
 
        def perferation():
            r = (CR123A_HEIGHT-base_thickness)/2
            return up(r + base_thickness)(
                        cube([x_length-4*min_wall, x_width+ABIT, x_height-4*min_wall], center=True) +
                        cube([x_length+ABIT, x_width-4*min_wall, x_height-4*min_wall], center=True) +
                        cube([18, x_width-4*min_wall, x_height+ABIT], center=True))

        return (up(x_height/2)(cube([x_length,x_width,x_height], True)) -
                    hole()(internal + screws))

    def casters(x):
        caster_offset = radius - caster_d
        return forward(caster_offset)(x) + back(caster_offset)(x)

    def motors(x):
        x2 = forward(radius - min_wall - wheel_w)(x)
        return rotate([0,0,90])(x2) + rotate([0,0,-90])(x2)

    def wheel_cutouts():
        wheel = up(base_thickness+5)(rotate([0, 90, 0])(cylinder(r=wheel_r+1, h=wheel_w, center=True)))
        wheel_offset = radius - min_wall - wheel_w/2
        return hole()(left(wheel_offset)(wheel) + right(wheel_offset)(wheel))

    def pen_cutout():
        return hole()(cylinder(d=12, h=100, center=True))

    return (# perimeter() +
            # base() +
            motors(pololu_motor_mount()) +
            casters(pololu_3_8_caster_mount()) +
            up(base_thickness/2)(cube([battery_box_length, 12, base_thickness], True)) +
            batteries(battery_box()) -
            (wheel_cutouts() +
             pen_cutout()))

def assembly():
    return chassis()
 
if __name__ == '__main__':
    out_dir = sys.argv[1] if len(sys.argv) > 1 else os.curdir
    file_out = os.path.join( out_dir, 'printedchassis.scad')
 
    a = assembly()
    print("%(__file__)s: SCAD file written to: \n%(file_out)s"%vars())
    # scad_render_to_file( a, file_out, include_orig_code=True)
    scad_render_to_file( a, file_out, file_header='$fa = %s; $fs = %s;' % (FA, FS), include_orig_code=True)
