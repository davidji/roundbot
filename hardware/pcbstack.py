
"""
Stack some small standard size pcb 'modules'
Stacking headers result in a spacing of ~12.8mm
I have some 30x70x1.6mm PCBs with M2 corner holes, 66x26mm
I want to put a connector at one end, so at the other
end I need some support.
"""

from solid import *
from solid.utils import *
import util, body, eyes, chassis
from util import radial, pipe, ABIT
from fixings import M3

SPACING=12.8

def spacer():
    return (linear_extrude(2)(square([30, 4], center=True)) +
            union()(
                *(translate([x, 0, 0])(
                    cylinder(h=3.6, d=2.0) +
                    up(3.6)(sphere(d=2.0)) +
                    down(18-1.6)(cylinder(h=(18-1.6), d=4.0) - sphere(d=2)))
                  for x in (+13, -13))))

def stack(layers, spacing = SPACING, pcb=(70.0, 30.0, 1.6)):
    brace = (
        linear_extrude(2.0)(
            square([pcb[0]-2.0, pcb[1]], center=True) - 
            forward(2.0)(square([pcb[0]-8.0, pcb[1]], center=True))))
    
    return (linear_extrude((layers-1)*spacing+8.0)(
            (square([pcb[0] + 4.0, pcb[1]], center=True) -
             square([pcb[0] - 2.0, pcb[1]], center=True)) +
            back(pcb[1]/2 + 1.0)(
                square([pcb[0] + 4.0, 2.0], center=True) -
                square([pcb[0] - 12.0, 2.0], center=True)) - 
            square([pcb[0] - 2.0, pcb[1]], center=True)) +
            union()(*(
                up(layer*spacing+3)(forward(ABIT)(hole()(linear_extrude(pcb[2])(square(pcb[0:2], center=True))))) + 
                up(layer*spacing)(brace + up(6.0)(brace) + linear_extrude(6.0+pcb[2])(back(pcb[1]/2 + 1.0)(
                    square([pcb[0] - 12.0, 2.0], center=True))))
                for layer in range(layers))))

def stackbodysides(layers):
    stackbody = eyes.eyes().body()
    stack_h = SPACING*layers+8.0
    return intersection()(
        stackbody.body_bounds(),
        (stackbody.side_module_blank() +
         mirror([1,0,0])(stackbody.side_module_blank()) +
           translate([0, stackbody.end_module_back() + 2.0, 17.0])(rotate([90, 0, 0])(stack(layers))) -
           stackbody.end_module_bounds() -
           mirror([0,1,0])(stackbody.end_module_bounds())))

def stackbody(layers):
    stackbody = body.body(height=32)
    stack_h = SPACING*(layers-1)+8.0
    return intersection()(
        stackbody.body_bounds(),
        (stackbody.body() +
         translate([0, stack_h/2, 17.0])(rotate([90, 0, 0])(stack(layers))) +
         union()(*[translate([0, y, 0])(linear_extrude(stackbody.height())(
             square([2*stackbody.radius(), 2], center=True) -
             square([70, 2], center=True)))
           for y in (stack_h/2-1, -stack_h/2+1)])))

def chassisplate(layers):
    stackchassis = chassis.chassis()
    stack_h = SPACING*(layers-1)+8.0
    return stackchassis.pcb_plate_blank() + translate([0, stack_h/2, 17.0])(rotate([90, 0, 0])(stack(layers)))

if __name__ == '__main__':
    util.save('pcbstack-spacer', spacer())
    util.save('pcbstack', stack(4))
    util.save('pcbstack-body-sides', stackbodysides(4))
    util.save('pcbstack-body', stackbody(3))
    util.save('pcbstack-chassis-plate', chassisplate(4))
