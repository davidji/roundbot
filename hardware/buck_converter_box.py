from solid import *
from solid.utils import *
import util
from util import origin, corners, ABIT
from fixings import M3
import boxes
from honeycomb import honeycomb

"""
Box for a micro-usb break out and a buck-boost
converter. There are access holes for the adjustment screw
and terminal screws.

"""

class converter:
    """3mm holes 30x46mm"""
    d = [34.2,61.5,14.0]
    dholes = [28.375, 55.25]


wall_thickness=2.0       

side_gap = 2.0
width = converter.d[0] + 2*side_gap
depth = converter.d[1]
lid_height=12.0
pcb_height = 4.0
height = pcb_height + lid_height
pcb_thickness=1.7

box = boxes.Box([width, depth, height], wall_thickness)

terminal_screw_hole = hull()(left(2.5)(circle(d=5)), right(2.5)(circle(d=5)))
terminal_screw_holes = (
    forward(converter.d[1]/2 - 4.0)(terminal_screw_hole) +
    back(converter.d[1]/2 - 4.0)(terminal_screw_hole))

terminal_wire_hole_height = height/2 - pcb_height - 3
terminal_wire_hole = back(terminal_wire_hole_height)(square([9,6], center=True))

def standoffs(standoff):
    return up(wall_thickness)(mirror([0,0,1])(union()(*(
        translate(p)(standoff)
        for p in corners(*converter.dholes)))))

screw_standoffs = standoffs(M3.screw_standoff(lid_height+wall_thickness))
nut_capture_standoffs = standoffs(M3.nut_capture_standoff(pcb_height+wall_thickness-pcb_thickness)) 

switch_spacing=(45.25+33.21)/2.0
switch_x = converter.d[0]/2 - 4
switch_height=4.75
switch_pusher_height = lid_height - switch_height

switch_button = (
    mirror([0,0,1])(left(switch_x)(cylinder(d=6, h=switch_pusher_height))) +
    box.hole()(
        (square([2*switch_x, 7], center=True) + left(switch_x)(circle(d=7))) - 
        (square([2*switch_x, 6], center=True) + left(switch_x)(circle(d=6)))))
switch_buttons = forward(switch_spacing/2)(switch_button) + back(switch_spacing/2)(switch_button)

display_height = 7.25
display_width = 22
display_depth = 14
display = (
    left((converter.d[0] - display_depth)/2)(
        (up(wall_thickness)(mirror([0,0,1])(
            linear_extrude(lid_height - display_height + wall_thickness)(
                offset(r=wall_thickness)(square([display_depth, display_width], center=True)) +
                hole()(square([display_depth, display_width], center=True))))))))

trim_y = converter.d[1]/2 - 35.3
trim_x = converter.d[0]/2 - 1.8
trim = box.hole()(translate([trim_x, trim_y])(circle(d=4)))

def label(s, valign="center", halign="center", depth=0.5):
    return up(wall_thickness-depth)(
        linear_extrude(depth+ABIT)(
            hole()(text(s, valign=valign, halign=halign, font="Noto Sans Mono CJK TC:style=Bold", size=8))))

vent_slot = box.hole()(hull()(forward(3.5)(circle(d=3)), back(3.5)(circle(d=3))))
vent_slots = union()(*(left(5*i)(vent_slot) for i in range(-2, 3)))
side_vent_slots = forward((height-lid_height)/2)(vent_slots)
top_vent_slots = right(5)(rotate([0,0,90])(vent_slots))

faces = {
    "top":(
        box.top.blank() + 
        box.hole()(terminal_screw_holes) +
        screw_standoffs +
        switch_buttons +
        display +
        top_vent_slots + 
        trim),
    "bottom":(
        box.bottom.blank() +
        nut_capture_standoffs),
    "left":(box.left.blank() +
              forward(3)(
              right(depth/2)(label("out", halign="right")) +
              left(depth/2)(label("in", halign="left")))),
    "right":(box.right.blank() + side_vent_slots),
    "front":(box.front.blank() + 
               box.hole()(terminal_wire_hole) + 
               forward(3)(
                   left(5)(label("+", halign="right")) +
                   right(5)(label("-", halign="left")))),
    "back":(box.back.blank() + 
            box.hole()(terminal_wire_hole) +
            forward(3)(
                left(5)(label("-", halign="right")) +
                right(5)(label("+", halign="left"))))
   }

def assembly():
    return box.top(height = components_height, **faces)

def export_scad():
    util.save('buck-converter-lid', box.above(height = lid_height, **faces))
    util.save('buck-converter-base', box.below(height = pcb_height, **faces))
    util.save('barrel-jack', BarrelJack.assembly())

if __name__ == '__main__':
    export_scad()
