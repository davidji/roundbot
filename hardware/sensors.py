from solid import *
from solid.utils import *

from util import radial, corners
from fixings import M1_6

class hc_sr04:
    """Ultrasonic rangefinder module
    The transmitter and receiver are two cylinders d=16 protruding from the front"""
    d = [45,20,16]
    
    @staticmethod
    def tranceiver_cut():
        return radial(18, [0,180], circle(r=8))

    @staticmethod
    def screw_cut(tapped=False):
        return corners([17.4,42.4], M1_6.cut(tapped))