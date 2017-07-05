from solid import *
from solid.utils import *
import util
from util import corners, vadd
from fixings import M2

class oled:
    d = [27.0, 28.0, 5.0]

    # Fixings are M2
    fixing = M2
    # square arrangement [23, 23]
    @staticmethod
    def fixings(center=False):
        return (center and corners(23.0, 23.0, center=True)
                or util.origin([2.0, 2.5])(*corners(23.0, 23.5, center=False)))

    class display:
        d = [26.0, 15.0]
        corner = [0.5, 5.0]
        center = vadd(corner, [x/2 for x in d])

        @staticmethod
        def origin(center=False):
            return center and util.origin([-x for x in center]) or util.origin(corner)

        @staticmethod
        def fixings(center=False):
            o = [-x for x in center and oled.display.center or corner]
            return util.origin(o)(*oled.fixings())


