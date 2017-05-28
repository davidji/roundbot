
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
    keystone 209 (or 5209?). They are not the only battery holder
    that uses these connectors. See: 
    https://www.thingiverse.com/thing:331394. I did look at that,
    and it's where I found out about this particular connector,
    but this code isn't really based on the above.
    This has a screw cover option. It's really designed to go
    on the bottom of a toy or robot, where that's necessary.
    """

    def __init__(self, 
                 cell_length, 
                 cell_diameter,
                 cell_count=None,
                 cell_offsets=None, 
                 wall_thickness=2.0, 
                 spring_thickness = 4.0):
        self.cell_length = cell_length
        self.spring_thickness = float(spring_thickness)
        self.cell_diameter = float(cell_diameter)
        self.wall_thickness = float(wall_thickness)
        self.d = [self.cell_diameter + 2*self.wall_thickness, 
                  self.cell_length + 2*self.wall_thickness, 
                  self.cell_diameter + 2*self.wall_thickness]
        if cell_count and not cell_offsets:
            self.cell_offsets = [(cell - cell_count/2.0 + 0.5)*cell_diameter for cell in range(cell_count)]
        elif cell_offsets and not cell_count:
            self.cell_offsets = cell_offsets
        else:
            raise ValueError("Specify one of cell_count, cell_offsets")


    def _terminal_spacing(self):
        return self.cell_length + 2 * self.spring_thickness

    def _cell_back(self):
        """This is the back shell for a single cell"""
        terminal_spacing = self._terminal_spacing()
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
            # half the height above the centre.
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
            # The shell, and everything it depends on is constructed vertically
            return (linear_extrude(center=True,
                                   height=terminal_spacing+2*self.wall_thickness)
                    (outer_profile()) +
                    battery_cavity() +
                    tab_slots())

        return up(shell_radius)(rotate([-90, 0, 0])(shell()))

    def back(self, t = 2.0):
        """Back shell for the panel holder"""
        return union()(*(translate([offset, 0, 0])(self._cell_back()) for offset in self.cell_offsets))

    def _cell_cutouts(self):
       return (translate([offset, 0, 0])(
           square([self.cell_diameter,
                   2*self.spring_thickness + self.cell_length], 
                  center=True))
               for offset in self.cell_offsets)

    def panel(self, flange = 6.0):
        return (linear_extrude(height=self.wall_thickness)(
            offset(delta=self.wall_thickness+flange)(
                hull()(*self._cell_cutouts())) + hole()(union()(*self._cell_cutouts()))) +
                hole()(self.screw_cover()))

    def _screw_positions(self, fixing):
        terminal_spacing = self._terminal_spacing()
        x = self.cell_offsets[-1] + self.cell_diameter/2 + self.wall_thickness + fixing.thread/2
        y = terminal_spacing/2 - fixing.thread
        return [[x, y], [x, -y]]

    def _screw_tabs_outline(self, fixing=M3):
        t = self.wall_thickness
        screw_tab = (translate([-fixing.thread - t, -fixing.thread])(square([fixing.thread + t, fixing.thread*2])) +
                     circle(r=fixing.thread))
        return union()(*(translate(p)(screw_tab) for p in self._screw_positions(fixing)))

    def _hook_positions(self, w):
        terminal_spacing = self._terminal_spacing()
        x = self.cell_offsets[0] - self.cell_diameter/2
        y = (terminal_spacing - w)/2
        return [[x, y], [x, -y]]

    def _cover_hooks(self, w):
        hook = translate([-self.wall_thickness, -w/2])(square([self.wall_thickness, w]))
        return hole()(up(self.wall_thickness)(linear_extrude(height=self.wall_thickness*1.5)(
            union()(*(translate(p)(hook) for p in self._hook_positions(w))))))

    def _screw_cover_outline(self, fixing):
        return (hull()(*self._cell_cutouts()) + 
                self._screw_tabs_outline(fixing))

    def screw_cover_mount(self, fixing=M3, inset_height=3.0, hook_width=7.0):
        return (
            linear_extrude(height=self.wall_thickness+inset_height)(
                offset(r=self.wall_thickness)(self._screw_tabs_outline(fixing)) -
                hole()(union()(*(translate(p)(circle(d=fixing.insert)) for p in self._screw_positions(fixing))))) +
            self.panel(0) +
            self._cover_hooks(hook_width) +
            hole()(linear_extrude(height=self.wall_thickness)(offset(delta=0.5)(self._screw_cover_outline(fixing)))))
    
    def screw_cover(self, fixing=M3, hook_width=7.0):
        t = self.wall_thickness
        hook = up(t)(linear_extrude(height=t)(square([2*t, hook_width-1.0], center=True)))
        return (
            linear_extrude(height=t)(
                self._screw_cover_outline(fixing) +
                hole()(union()(*(translate(p)(fixing.cut()) for p in self._screw_positions(fixing)))) -
                right(self.cell_offsets[-1] + self.cell_diameter/2)(circle(d=10.0))) +
            union()(*(translate(p)(hook) for p in self._hook_positions(hook_width))))
    