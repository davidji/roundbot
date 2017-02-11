
from solid import *
from solid.utils import *

from util import inch_to_mm, pipe
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
        

class MetricThread(AnyThread):
    def __init__(self, thread, tap, insert=None):
        AnyThread.__init__(self, thread, tap, insert)
        self.nut = MetricNut(thread)


M1_6 = MetricThread(1.6, 1.25)
M2 = MetricThread(2.0, 1.6, 3.6)
M2_5 = MetricThread(2.5, 2.05, 3.8)
M3 = MetricThread(3.0, 2.5, 4.0)


"""https://www.pololu.com/product/989, the screws are 2-56 with diameter 2.184mm"""
NO2 = AnyThread(inch_to_mm(0.08), inch_to_mm(0.08))
NO2.nut = Nut(inch_to_mm(3.0/16), inch_to_mm(1.0/16))