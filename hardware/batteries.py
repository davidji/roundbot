
from solid import *
from solid.utils import *
from util import inch_to_mm, tube, ABIT

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




class PanelHolder:
    """These holders are based on a pair of spring contacts:
    keystone 209 (or 5209?). There's also provision to hold the 
    battery in with a 10mm hook and loop strap. In my application
    that's more convenient than a screw cover.
    """

    def __init__(self, cell_length, cell_diameter, wall_thickness=2.0, spring_thickness = 4.0):
        self.cell_length = cell_length
        self.spring_thickness = float(spring_thickness)
        self.cell_diameter = float(cell_diameter)
        self.wall_thickness = float(wall_thickness)
        self.d = [self.cell_diameter + 2*self.wall_thickness, 
                  self.cell_length + 2*self.wall_thickness, 
                  self.cell_diameter + self.wall_thickness]
    

    def body(self, t = 2):

        terminal_spacing = self.cell_length + 2*self.spring_thickness
        cell_radius = self.cell_diameter/2
        shell_radius = cell_radius + self.wall_thickness

        def battery_cavity_profile():
            d = self.cell_diameter
            return circle(r=cell_radius) + translate([-cell_radius, 0])(square([d, cell_radius + ABIT]))
        
        def outer_profile():
            ir = cell_radius
            d = 2*shell_radius
            return (
                intersection()(
                    circle(r=shell_radius), 
                    translate([-shell_radius, -shell_radius])(square([d, shell_radius]))) +
                    translate([-shell_radius, 0])(square([d, ir])))
        
        def battery_cavity():
            return hole()(linear_extrude(center=True, height=terminal_spacing)(battery_cavity_profile()))
        
        def tab_slots():
            t = self.wall_thickness
            edge_t=1.6 # mm edge thickness specified by keystone 209
            ear_t = inch_to_mm(0.062) + 1
            tab_t = inch_to_mm(0.25)
            width=8.0 # mm width of keystone 209
            height=inch_to_mm(0.449)
            r = cell_radius
            # Getting the contact in the middle is about getting the edge
            # the connector sits on the right height. The edge needs to be
            # half the height above the center.
            tab = mirror([0,1,0])(
                translate([-width/2, height/2, -tab_t])(
                    cube([width, shell_radius - height/2, edge_t + ear_t + tab_t])) +
                up(edge_t + ear_t/2)(cube([width, height, ear_t], center=True)))
            return hole()(up(terminal_spacing/2)(tab) +
                    down(terminal_spacing/2)(mirror([0, 0, 1])(tab)))
        
        def velcro_slot():
            d = self.d[0] + ABIT
            return hole()(linear_extrude(height=10, center=True)(
                translate([-d/2, 0, 0])(square([d, cell_radius + ABIT]))))
        
        def shell():
            return (linear_extrude(center=True,
                                   height=terminal_spacing+2*self.wall_thickness)
                    (outer_profile()) +
                    battery_cavity() +
                    tab_slots() +
                    velcro_slot())


        return up(cell_radius)(rotate([-90, 0, 0])(shell()))

