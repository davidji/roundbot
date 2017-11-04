
import sys, os.path
from solid import *
from batteries import *
import util
from fixings import M3

FA=0.1
FS=0.5

radius = 12.0
length = 150

def switch_hole():
    return hole()(
        down(radius)(linear_extrude(radius-10)(square([15.0, 22], center=True))) +
        down(10)(linear_extrude(1.5)(square([12.1, 19.3], center=True))) +
        down(8.5)(linear_extrude(10.5)(square([15.0, 24.0], center=True))) +
        up(2.0)(linear_extrude(9)(square([8, 24], center=True))))


star = up(13.22/2)(import_stl('wand-bottom-star.stl'))

def wand_handle():
    # cells = 2
    # cell_length = 44.5
    # cell_diameter = 10.75
    cells = 1
    cell_length = 34.7
    cell_diameter = 17.0
    batteries = InternalHolder(cell_length=cells*cell_length, cell_diameter=cell_diameter, cell_count=1,wall_thickness=1.5)
    screw = intersection()(
        rotate([90, 0, 0])(cylinder(r=radius, h=10, center=True)), 
        down(radius)(M3.nut_capture_standoff(h=radius)) + up(radius)(rotate([180,0,0])(M3.screw_standoff(h=radius-4, screw_head_h=4))))
    
    wire = hole()(
        right(cell_diameter/2)(rotate([-90, 0, 0])(linear_extrude(batteries.d[1]+8, center=True)(square([1.5,1.5])))) +
        down(1.5)(forward((batteries.d[1]+8)/2-1.5)(cube([cell_diameter/2, 1.5, 1.5])) +
                  back((batteries.d[1]+8)/2)(cube([cell_diameter/2, 1.5, 1.5]))))
    
    return (
        rotate([-90, 0, 0])(util.tube(r=radius, ir=5, h=length, center=True) + down(length/2)(cylinder(r=radius, h=2))) +
        back(length/2 - batteries.d[1]/2 - 16)(
            mirror([0,0,1])(down(batteries.d[2]/2)(batteries.back())) +
            down(radius)(hole()(linear_extrude(radius)(square([cell_diameter, batteries.d[1]], center=True)))) +
            forward(batteries.d[1]/2 + 28)(switch_hole()) +
            wire) +
        forward(length/2+30)(hole()(star + mirror([0,0,1])(star))) +
        back(length/2-6)(screw) +
        forward(length/2-20)(screw))

def wand_handle_top():
    return intersection()(
        wand_handle(),
        linear_extrude(radius)(square([radius*2, length], center=True)))

def wand_handle_bottom():
    return intersection()(
        wand_handle(),
        down(radius)(linear_extrude(radius)(square([radius*2, length], center=True))))


def export_scad():
    util.save('wand-handle-top', wand_handle_top())
    util.save('wand-handle-bottom', wand_handle_bottom())
    util.save('wand-star-centered', star)
        
if __name__ == '__main__':
    export_scad()
