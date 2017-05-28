from solid import *
from solid.utils import *

import fixings
from util import corners

class aplus:
    d = [65,56,10]

    @staticmethod
    def cut_holes():
        return corners(58,49)(fixings.M2_5.cut())

class zero:
    d = [65.0, 30.0]
    h = [58.0,23.0]
    holes = corners(*h)
    fixing = fixings.M2_5
