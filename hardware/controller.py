
import util, joystick, boxes, batteries, usb
from util import inch_to_mm, corners, tube, ABIT
from fixings import M3
from solid import *
from solid.utils import *
from display import oled

def controller():
    t = 2.0
    r = 5.0
    w = 35.0*2 + 32 - 2*r + 3
    d = 80.0
    h = 20.0

    def shell():
        return boxes.roundbox([w, d, h], r, t)
    
    def outside_bounds(a):
        return intersection()(boxes.roundcube([w, d, h], r), a)

    def inside_bounds(a):
        return intersection()(boxes.roundcube([w, d, h], r-t), a)

    def split(z, a):
        return intersection()(a, up(z)(cube([x + 2*r for x in (w, d, h)], center=True)))

    def joysticks(a):
        return back(d/2+3-16.0)(
            left(w/2.0+r-17.5-1)(a) +
            right(w/2.0+r-17.5-1)(a))

    base = h/2+r-t
    pw = M3.nut.f+2.0
    ph = h+2*(r - t)

    def panel():
        return up(h/2 + r - t)
    
    def panelhole(a):
        return hole()(panel()(down(ABIT)(linear_extrude(t+2*ABIT)(a))))
    
    battery_factory = batteries.PanelHolder(cell_length=34.5, cell_diameter=17.0, cell_count=1)
    battery = panel()(translate([0, d/2+r-t-15.5, t])(
        mirror([0,0,1])(
        rotate([0,0,-90])(
            battery_factory.back() + 
            battery_factory.screw_cover_mount()))))

    pillar_locations = (
        ([-w/2 + M3.thread, +d/2 - M3.thread], 0),
        ([+w/2 - M3.thread, +d/2 - M3.thread], 0),
        ([-w/2 + M3.thread, -d/2 + 35.0 - r + M3.thread + 1.0], 180),
        ([+w/2 - M3.thread, -d/2 + 35.0 - r + M3.thread + 1.0], 180))

    def pillars():
        pillar = up(h/2 + r)(mirror([0,0,1])(
            linear_extrude(r)(circle(r=2*M3.thread)) +
            linear_extrude(h+r)(circle(r=M3.thread)) +
            hole()(
                linear_extrude(h+r)(M3.cut()) +
                linear_extrude(M3.thread)(circle(r=M3.thread)))))
        return inside_bounds(
            union()(*(translate(t)(rotate([0,0,r])(pillar)) for (t,r) in pillar_locations)))

    def screw_holes():
        return down(base + t)(
            *(translate(t)((linear_extrude(r)(circle(r=2*M3.thread) + hole()(M3.cut()))) + hole()(M3.nut.capture())) 
              for (t,_) in pillar_locations))

    def nodemcu_usb():
        height = h + r - t - 1.6
        return hole()(translate([0, -d/2-r, h/2-height+1.6])(
            mirror([0,0,1])(rotate([0,0,90])(linear_extrude(2*t, center=True)(usb.micro.cut())))))

    def nodemcu():
        height = h + r - 2*t - 1.6
        return (
            translate([0, d/2+r-t-15.5, h/2 + r - t - height])(
                union()(*(
                    translate(p)(tube(ir=M3.thread/2, r=M3.insert/2+1.0, h=height) -
                                 cylinder(d=M3.insert, h=3.0))
                        for p in corners(*inch_to_mm([2.0,1.0]))))))

    def powerswitch():
        height = 14.0
        return back(d/2 + r - t - inch_to_mm(0.5))(
            panelhole(circle(d=10.0)) +
            panel()(mirror([0,0,1])(
                linear_extrude(height)(
                    square([x + 1.0 for x in inch_to_mm([1.0,1.0])], center=True) - 
                    square([x - 1.0 for x in inch_to_mm([1.0,1.0])], center=True)) +
                linear_extrude(height+1.6)(
                    square([x + 1.0 for x in inch_to_mm([1.0,1.0])], center=True) -
                    square([x + 0.1 for x in inch_to_mm([1.0,1.0])], center=True)) -
                linear_extrude(height+1.6)(
                    offset(r=1.0)(square(inch_to_mm([0.5,1.0]), center=True))))))

    def powerswitchback():
        height = ph - 14.0 - 1.6
        board_outline = square(inch_to_mm([1.0,1.0]), center=True)
        return translate([0, -d/2 - r + t + inch_to_mm(0.5), -base])(
                linear_extrude(height)(
                    offset(r=1.0)(board_outline) - 
                    offset(r=-1.0)(board_outline)))

    def displayposition():
        def transform(a):
            return back(d/2 + r - t - inch_to_mm(1.0) - 3.0 - oled.d[1]/2)(
                rotate([0,0,180])(a))
        return transform

    def display():
        return displayposition()(
                panelhole(square(oled.display.d, center=True)) +
                panel()(mirror([0,0,1])(
                    union()(*(translate(p)(cylinder(d=3, h=1.6) + cylinder(d=2, h=2.8))
                              for p in oled.display.fixings(center=True))))))

    def displayback():
        return displayposition()(
            down(base)(
                    union()(*(translate(p)(cylinder(d=3, h=ph-2.8) + cylinder(d=5, h=ph-4.0))
                              for p in oled.display.fixings(center=True)))))

    def gyromount():
        return panel()(mirror([0,0,1])(
            union()(*(translate(p)(cylinder(d=5, h=10.0) + cylinder(d=3, h=12.0))
                      for p in corners(40.0, 10.0)))))

    def gyromountback():
        return down(base)(
            union()(*(translate(p)(cylinder(d=5, h=ph - 12.0))
                      for p in corners(40.0, 10.0))))

    class Controller:
        def top(self):
            return outside_bounds(
                split(r, shell()) +
                up(h/2+r)(joysticks(joystick.block())) +
                battery +
                nodemcu() +
                powerswitch() +
                display() +
                gyromount() +
                pillars())

        def bottom(self):
            return outside_bounds(
                split(-h-r, shell()) +
                screw_holes() +
                inside_bounds(
                    powerswitchback() +
                    displayback() +
                    gyromountback() +
                    down(base)(
                        joysticks(
                            union()(*(translate(p)(
                                cylinder(d=joystick.fixing.thread*2, h=h+ 2*r - t - joystick.height))
                                for p in joystick.fixings()))))))

    return Controller()

def export_scad():
    util.save('controller-top', controller().top())
    util.save('controller-bottom', controller().bottom())

if __name__ == '__main__':
    export_scad()