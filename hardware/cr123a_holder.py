
import sys, os.path
from solid import *
from batteries import *

FA=0.1
FS=0.5

def assembly():
    holder = PanelHolder(cell_length=34.5, cell_diameter=17.0)
    return holder.body()

if __name__ == '__main__':
    out_dir = sys.argv[1] if len(sys.argv) > 1 else os.curdir
    file_out = os.path.join( out_dir, 'cr123a_holder.scad')
 
    a = assembly()
    print("%(__file__)s: SCAD file written to: \n%(file_out)s"%vars())
    scad_render_to_file( a, file_out, file_header='$fa = %s; $fs = %s;' % (FA, FS), include_orig_code=True)
