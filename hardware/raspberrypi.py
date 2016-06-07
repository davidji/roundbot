from solid import *
from solid.utils import *

import fixings
from util import corners

class aplus:
    d = [65,56,10]

    @staticmethod
    def cut_holes():
        return corners([58,49], fixings.M3.cut())
