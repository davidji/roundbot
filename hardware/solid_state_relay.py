
from solid import *
from solid.utils import *
from util import *
from honeycomb import honeycomb, hexagon
from fixings import M3
from math import sqrt
from nodemcu import NodeMcuV3
import usb

class SwitchedFusedIecConnector:
    body_w = 47
    body_d = 27.5
    body_h = 17.5
    body_c = 6.0
    body_points = [
        [ body_w/2 - body_c,  body_d/2],
        [ body_w/2,  body_d/2 - body_c],
        [ body_w/2, -body_d/2 + body_c],
        [ body_w/2 - body_c, -body_d/2],
        [-body_w/2, -body_d/2],
        [-body_w/2,  body_d/2] ]

    panel_w = 50.5
    panel_d = 31.25
    panel_h = 3.3
    panel_r = 2.5

    clips1_w = 10.0
    clips1_x = - body_w/2 + 7.5
    clips2_w = 7.0
    clips2_x = body_w/2 - 12.5
    clips_d = 30.0
    clip_t = 0.8

    @classmethod
    def body(self):
        return down(self.panel_h + self.body_h)(linear_extrude(self.body_h)(polygon(self.body_points)))
    
    @classmethod
    def panel(self):
        return down(self.panel_h)(linear_extrude(self.panel_h)(stadium([self.panel_w, self.panel_d], self.panel_r)))
    
    @classmethod
    def clips(self):
        return down(self.panel_h + self.body_h)(
            linear_extrude(self.body_h - self.clip_t)(
                right(self.clips1_x)(square([self.clips1_w, self.clips_d], center=True)) +
                right(self.clips2_x)(square([self.clips2_w, self.clips_d], center=True))))

    @classmethod
    def assembly(self):
        return self.body() + self.panel() + self.clips()

class Heatsink:
    d = [37.0, 37.0, 12.0]
    screw_spacing = 30.0

class EuroModule:
    panel_w=50.0
    panel_t=5.0
    clip_w=45.0
    clip_t=4.0
    
    rail_points = [[(panel_w - clip_w)/2, panel_t+clip_t],
                   [0, panel_t],
                   [0, 0],
                   [-panel_t, 0],
                   [-panel_t, panel_t],
                   [0, panel_t+clip_t]]
    
    @classmethod
    def rail_section(self):
        return polygon(self.rail_points)

    @classmethod
    def rails_section(self):
        return (left(self.panel_w/2)(self.rail_section()) +
                right(self.panel_w/2)(mirror([1,0,0])(self.rail_section())) +
                hole()(left(self.panel_w/2)(square([self.panel_w, self.panel_t]))))

    @classmethod
    def rails(self, n):
        return rotate([90, 0, 0])(linear_extrude(n*self.panel_w, center=True)(self.rails_section()))

class SsrModule:
    d = [30, 80, 28]
    screws = [25.0, 74.5]

panel_w = 55.0
panel_h = 80.0
panel_t = 4.0

lip = 1.0

def box_assemblies(length, width=panel_h+6, wall_t=2.0, fixing=M3):
    
    id = [length, width, panel_w + 2*lip]

    olength = length + 2*(panel_t + wall_t)
    owidth = width + 2*(panel_t + wall_t)
    oheight = (panel_w + 2*(wall_t+lip))
    od = [olength, owidth, oheight]
    
    standoff_h = 8.0
    
    def standoff():
        return rotate([0,0,90])(M3.nut_capture_standoff(8))

    def blank_panel(w=panel_w, h=panel_h, t=panel_t):
        return (down(4.0)(linear_extrude(2.0)(square([w+2.0,h+2*lip], center=True))) +
                down(t)(linear_extrude(t)(square([w,h], center=True))))
    
    def inside():
        end = rotate([0, -90, 0])(blank_panel(t=panel_t + wall_t + 2.0))
        return (left(length/2 + ABIT)(end) +
                right(length/2 + ABIT)(rotate([0,0,180])(end)))
    
    def shell():
        end = rotate([0, -90, 0])(blank_panel(t=panel_t + wall_t + 2*ABIT))
        side = rotate([0, -90, -90])(blank_panel(t=panel_t + wall_t + 2*ABIT))
        return up(od[2]/2)(intersection()(
            down(od[2]/2)(cube(od, center=True)),
            cube(od, center=True) - (
                cube(id, center=True) +
                left(olength/2 + ABIT)(end) +
                right(olength/2 + ABIT)(rotate([0,0,180])(end)) +
                forward(owidth/2 + ABIT)(side) +
                back(owidth/2 + ABIT)(rotate([0,0,180])(side)))))

    def ssr_module_offset():
        return (length - SsrModule.d[0]) / 2 - 30

    def nodemcu_module_offset():
        return (length - NodeMcuV3.d[0])/2 - 22

    def bottom_shell():
        flange = back(6)(left(6)(cube([12,12,8])) - left(4)(up(4)(cube([8,12,4])))) - cylinder(d=fixing.thread, h=4.0)
        return (shell() +
                union()(*(translate(p)(flange) for p in corners(length-20, owidth+12))) +
                left(ssr_module_offset())(
                    union()(*(translate(p)(standoff()) for p in corners(*SsrModule.screws)))) +
                right(nodemcu_module_offset())(
                    forward((width - NodeMcuV3.d[1])/2)(
                    union()(*(translate(p)(standoff())
                              for p in corners(*NodeMcuV3.screws))))) +
                up(oheight/2-1)(hole()(linear_extrude(1.0)(square([length+4, width+4], center=True) - square([length, width], center=True)))) +
                union()(*(translate(p)(
                    rotate([0,0,90])(fixing.nut_capture_standoff(h=oheight/2, nut_capture_h=oheight/2-wall_t)))
                    for p in corners(length-20, width))))
    
    def ssr_vent_width():
        return SsrModule.d[0]*1.5
    
    def top_shell():
        return (shell() +
                right(nodemcu_module_offset())(
                    back(width/2 - 17.0)(
                    standoff())) +
                left(ssr_module_offset())(
                    hole()(linear_extrude(wall_t)(
                            honeycomb(4.0, 1.0, ssr_vent_width(), width - 10, center=True, inverted=True)))) +
                union()(*(translate(p)(
                    rotate([0,0,90])(fixing.screw_standoff(h=oheight)))
                    for p in corners(length-20, width))))
    
    def inlet_panel():
        thickness = SwitchedFusedIecConnector.panel_h + 2.0
        w = panel_w
        d = panel_h
        relay_forward = (d - Heatsink.d[1] - 5)/2
        relay_standoff_h = 12.0
        r = 4.0
        R=(2.0*r)/sqrt(3.0)
        return (blank_panel(t=thickness) +
                back((d - SwitchedFusedIecConnector.panel_d - 5)/2)(
                    hole()(SwitchedFusedIecConnector.assembly()))  -
                forward(relay_forward)(
                    down(thickness)(
                        linear_extrude(thickness)(
                            honeycomb(4.0, 1.0, w-5.0, Heatsink.d[1], center=True, inverted=True)))) +
                forward(relay_forward)(mirror([0, 0, 1])(
                    linear_extrude(thickness)(forward(3*R)(hexagon(4.0)) + back(3*R)(hexagon(4.0))) +
                    up(thickness)(forward(Heatsink.screw_spacing/2)(M3.insert_standoff(relay_standoff_h)) +
                                  back(Heatsink.screw_spacing/2)(M3.insert_standoff(relay_standoff_h))))))
    
    def outlet_panel():
        return mirror([0,0,1])(blank_panel()) + rotate([0,0,90])(EuroModule.rails(1))

    def vent_panel():
        return (blank_panel() +
                down(panel_t)(forward(ssr_module_offset())(
                    hole()(linear_extrude(panel_t)(
                        honeycomb(4.0, 1.0, panel_w - 5, ssr_vent_width(), center=True, inverted=True))))))

    def io_panel():
        pcb_height = panel_w / 2 - 8 + lip + wall_t
        return (vent_panel() + 
                back(nodemcu_module_offset())(
                    down(panel_t)(hole()(
                        left(pcb_height)(
                            back(8)(linear_extrude(panel_t)(square([14,16])))) +
                        right(pcb_height)(
                            right(1)(up(1.5)(linear_extrude(panel_t-1.5)(square([8,14], center=True)))) +
                            linear_extrude(panel_t)(offset(r=0.6)(usb.micro.cut())))))))

    return {
        'solid-state-relay-inlet-panel': inlet_panel(),
        'solid-state-relay-outlet-panel': outlet_panel(),
        'solid-state-relay-shell': shell(),
        'solid-state-relay-bottom-shell': bottom_shell(),
        'solid-state-relay-top-shell': top_shell(),
        'solid-state-relay-vent-panel':  vent_panel(),
        'solid-state-relay-io-panel':  io_panel() }

def export_scad():
    save('switched-fused-iec', SwitchedFusedIecConnector.assembly())
    for name, assembly in box_assemblies(120).items():
        save(name, assembly)

if __name__ == '__main__':
    export_scad()
