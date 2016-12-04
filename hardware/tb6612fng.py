
# This module is for various tb6612fng carrier boards

from util import inch_to_mm, FA, FS
from solid import *
from solid.utils import *

class jst:
    enclosure = [ 6.0, 6.0, 4.75 ]


class generic_tb6612fng:
    pcb = [ inch_to_mm(0.8), inch_to_mm(0.8), inch_to_mm(0.005) ]
    """These are the dimensions of the pcb only, rather than a bounding box around the components"""

    d = [ inch_to_mm(0.8), inch_to_mm(0.8), 4 ]
    """This is a bounding box for the module"""
    
    @staticmethod
    def holder(data_wire=1.5, power_wire=1.6):
    
        """This part holds the module, and various connectors and wires:
        There are st-ph connectors for the motors, and tunnels for the
        control and power wires.
        
        The board fits in the box with the components facing down, and
        the labels facing up for convenience"""
        d = generic_tb6612fng.d
        base_z = 2.0
        wall_y = 2.0
        wall_x = jst.enclosure[0]
        height = d[2] + base_z + 4.0
        return (cube([d[0] + 2*wall_x, d[1] + 2*wall_y, height]) -
                translate([wall_x, wall_y, base_z])(cube([d[0], d[1], height - base_z])))
        
if __name__ == '__main__':
    out_dir = sys.argv[1] if len(sys.argv) > 1 else os.curdir
    file_out = os.path.join( out_dir, 'tb6612fng.scad')
 
    a = generic_tb6612fng.holder()
    print("%(__file__)s: SCAD file written to: \n%(file_out)s"%vars())
    scad_render_to_file( a, file_out, file_header='$fa = %s; $fs = %s;' % (FA, FS), include_orig_code=True)
