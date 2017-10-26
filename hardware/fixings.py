
from solid import *
from solid.utils import *

from util import inch_to_mm, pipe, tube
from honeycomb import hexagon

tolerance = 1.05

class Nut:
    def __init__(self, f, h):
        self.f  = f
        self.h = h

    def outline(self):
        return hexagon(r=self.f/2)
    
    def capture(self, h=None):
        h = h or self.h*1.2
        return linear_extrude(height=h)(offset(0.6)(self.outline()))
    
    def side_capture(self, depth):
        return linear_extrude(height=self.h*1.1)(
            offset(self.f/20)(
                hull()(self.outline(), back(depth)(self.outline()))))

class MetricNut(Nut):
    def __init__(self, d):
        Nut.__init__(self, d*1.6, d*0.8)
        
class AnyThread:
    def __init__(self, thread, tap, insert=None):
        self.thread = thread
        self.tap = tap
        self.insert=insert

    def cut(self, tapped=False):
        return circle(r=(tapped and self.tap or self.thread*tolerance)/2)
    
    def standoff(self, h, center=False):
        return pipe(h, ir=float(self.tap)/2, r=float(self.thread), center=center)
    
    def insert_standoff(self, h, insert_h=3.0):
        return (
            pipe(h=h,
                 ir=self.thread/2.0, 
                 r=self.insert/2.0+1.0) +
             up(h-insert_h)(hole()(cylinder(d=self.insert, h=insert_h))))
        

class MetricThread(AnyThread):
    def __init__(self, thread, tap, insert=None):
        AnyThread.__init__(self, thread, tap, insert)
        self.nut = MetricNut(thread)

    def nut_capture_standoff(self, h, nut_capture_h=None):
        nut_capture_h = nut_capture_h or self.nut.h
        t = self.thread/2
        return (linear_extrude(nut_capture_h + t)(offset(r=t)(self.nut.outline())) +
                hole()(self.nut.capture(h=nut_capture_h)) +
                pipe(ir=self.thread/2, t=t, h=h))

    def screw_standoff(self, h, screw_head_h=None):
        screw_head_h = screw_head_h or 0.6*self.thread
        t = self.thread/2
        return (cylinder(d=2*(self.thread+t), h=screw_head_h+t) +
                hole()(cylinder(d=2*self.thread, h=screw_head_h)) +
                pipe(ir=self.thread/2, t=t, h=h))

def snapin(d1, d2, t, h1, h2):
    return (
        cylinder(d=d2, h=h1) +
        up(h1)(cylinder(d=d1, h=t)) +
        up(h1+t)(cylinder(d1=d1, d2=d2, h=h2/2)) +
        up(h1+t+h2/2)(cylinder(d1=d2, d2=d1)) +
        hole()(linear_extrude(h1+t+h2)(square([d2, d1/2], center=True)) +
               (tube(ir=d2/2.0, t=1.0, h=h1) - 
                linear_extrude(1.0)(square([d2/2, d2+2.0], center=True)))))

M1_6 = MetricThread(1.6, 1.25)
# M2 - the insert size is meant to be 3.6 but I'm finding that 
# a bit loose, so I've set it at 3.5 for now
M2 = MetricThread(2.0, 1.6, 3.5) 
M2_5 = MetricThread(2.5, 2.05, 3.8)
M3 = MetricThread(3.0, 2.5, 4.0)


"""https://www.pololu.com/product/989, the screws are 2-56 with diameter 2.184mm"""
NO2 = AnyThread(inch_to_mm(0.08), inch_to_mm(0.08))
NO2.nut = Nut(inch_to_mm(3.0/16), inch_to_mm(1.0/16))
