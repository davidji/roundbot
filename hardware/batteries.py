
from solid import *
from solid.utils import *

from fixings import M3

class cr123a:
    """ This is a specific CR123A battery holder from Spiratronics
    This is intended to be PCB mount. I'm just going to solder wires onto
    the tables, wrap them in shrinkwrap, and they will go though holes in
    the chassis. The index hole is meant to be 1.8mm. No doubt a 2mm hole will do
    From the Spiratronics provided datasheet:
    http://www.spiratronics.com/data/3785.pdf"""

    d = [43.2, 18.0, 18.0]

    @staticmethod
    def cut_holes(tapped=False):
        """Mounting holes in a flat surface (2D). If you want the """
        fixing_screw = M3.cut(tapped)
        fixing_screw_offset = 12.1
        fixing_screws = (left(fixing_screw_offset)(fixing_screw) +
                         right(fixing_screw_offset)(fixing_screw))
        terminal_hole = circle(d=3.0)
        terminal_offset = 38.0/2
        terminal_holes = (left(terminal_offset)(terminal_hole) +
                          right(terminal_offset)(terminal_hole))
        id_hole = translate([38.0/2, 8.2])(circle(d=1.8))
        return (fixing_screws + terminal_holes + id_hole)

    @staticmethod
    def cut_opening():
        """Opening for inserting batteries in a flat surface"""
        return square(cr123a.d[0:2], True)
