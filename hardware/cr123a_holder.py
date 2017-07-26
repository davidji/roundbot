
import sys, os.path
from solid import *
from batteries import *
import util

FA=0.1
FS=0.5

def assembly(cells):
    holder = PanelHolder(cell_length=34.5, cell_diameter=17.0, cell_count=cells)
    return holder.back() + holder.screw_cover_mount()

def export_scad():
    for cells in range(1, 5):
        holder = PanelHolder(cell_length=34.5, cell_diameter=17.0, cell_count=cells)
        util.save('cr123a-holder-{}'.format(cells), holder.back() + holder.screw_cover_mount())
        util.save('cr123a-cover{}'.format(cells), holder.screw_cover())
        
if __name__ == '__main__':
    export_scad()