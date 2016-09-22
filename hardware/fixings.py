
from solid import *
from solid.utils import *

from util import inch_to_mm

tolerance = 1.05

class MetricScrew:
    def __init__(self, thread, tap):
        self.thread = thread
        self.tap = tap

    def cut(self, tapped=False):
        return circle(r=(tapped and self.tap or self.thread*tolerance)/2)

M1_6 = MetricScrew(1.6, 1.25)
M2 = MetricScrew(2.0, 1.6)
M2_5 = MetricScrew(2.5, 2.05)
M3 = MetricScrew(3.0, 2.5)

"""https://www.pololu.com/product/989, the screws are 2-56 with diameter 2.184mm"""
NO2 = MetricScrew(inch_to_mm(0.08), inch_to_mm(0.08))