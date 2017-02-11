from solid import *
from solid.utils import *

from fixings import M3
from util import corners, inch_to_mm, vadd

class nucleo64:
    d = [70,57.54,10]

    tenth = inch_to_mm(0.1)

    """In the nucleo 64 spec, there's a sort of origin, which is the A5 pin in CN9.
    This components centre is the middle of the bounding box around the nucleo board.
    This vector is the offset from the centre of the component to the origin in the spec
    """
    origin = [ 10.87 - d[0]/2, 3.04 - d[1]/2]

    cn8 = origin
    cn9 = vadd([48.26, 0], origin)
    cn6 = vadd(cn8, [0, tenth*7])
    cn5 = vadd(cn9, [0, tenth*7+4.06])

    holes = [
        vadd(cn6, [0, tenth*7+13.97]),
        vadd(cn5, [0, tenth*9+3.56]),
        vadd(origin, [33.02, -tenth])]

    @staticmethod
    def cut_holes():
        return union()(*(translate(pos)(M3.cut()) for pos in nucleo64.holes))

