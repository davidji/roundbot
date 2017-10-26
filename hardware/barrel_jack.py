from solid import *
from solid.utils import *
import util
from util import origin, corners, ABIT
from fixings import M3
import boxes

class BarrelJack:
    hole_spacing = 20.4 - 9.0

    @classmethod
    def barrel(cls):
        return linear_extrude(7.0)(hull()(
            forward((11.7-(11.7-4.55))/2)(square([9.1,11.7-4.55], center=True)), 
            back((11.7-9.1)/2)(circle(d=9.1))))

    @classmethod
    def base(cls):
        return down(2.15)(linear_extrude(2.15)(hull()(
            forward(cls.hole_spacing/2)(circle(d=9.1)),   
            back(cls.hole_spacing/2)(circle(d=9.1)))))

    @classmethod
    def back(cls):
        return down(10)(linear_extrude(9)(square([9, 9.5], center=True)))

    @classmethod
    def assembly(cls):
        return cls.base() + cls.barrel() + cls.back()

wall_thickness = 2.0

def switch_box():
    width = 35.0
    depth = 25.0
    height = 20.0
    
    wall_thickness = 2.0
    
    box = boxes.Box([width, depth, height], wall_thickness)

    faces = {
        "top":(
            box.top.blank() + 
            box.hole()(square([12.1, 19.3], center=True))),
        "bottom":(
            box.bottom.blank()),
        "left":(box.left.blank() +
                hole()(BarrelJack.assembly()) +
                down(4.0)(linear_extrude(4.0)(square([14, height], center=True)))),
        "right":(box.right.blank() + box.hole()(circle(d=8))),
        "front":(box.front.blank()),
        "back":(box.back.blank())
        }

    util.save('barrel-jack-switch-lid', rotate([180, 0, 0])(box.above(height = height/2, **faces)))
    util.save('barrel-jack-switch-base', box.below(height = height/2, **faces))

def pairtoggle(wire_thickness=1.5, hole_diameter=8.0):
    lip_d = hole_diameter+2
    height=wall_thickness+10*wire_thickness
    rib = cylinder(d=lip_d, h=wire_thickness)
    rib_spacing = wire_thickness*2
    truss = linear_extrude(rib_spacing)(square([wire_thickness, 10], center=True))
    return rotate([0,90,0])(
        intersection()(
            cylinder(d=lip_d, h=1) + 
            up(1)(cylinder(d=hole_diameter*0.95, h=wall_thickness)) +
            up(1+wall_thickness)(
                intersection()(
                    cylinder(d1=10.0, d2=5.0, h=10*wire_thickness),
                    union()(*(up(r*rib_spacing)(rib) for r in range(5))) +
                    union()(*(rotate([0,0,90*(r%2)])(up(r*rib_spacing)(truss)) for r in range(4))))),
            linear_extrude(height)(
                left(lip_d/4)(square([lip_d/2,lip_d], center=True)))) +
        hole()(linear_extrude(height)(offset(r=wire_thickness/5)(hull()(
            left(wire_thickness/2)(circle(d=wire_thickness)) + 
            right(wire_thickness/2)(circle(d=wire_thickness)))))))

def export_scad():
    switch_box()
    util.save('barrel-jack', BarrelJack.assembly())
    util.save('barrel-jack-toggle', pairtoggle())

if __name__ == '__main__':
    export_scad()
