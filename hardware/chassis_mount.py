
from solid import *
from solid.utils import *
import util
from chassis import chassis
from fixings import M2, M2_5, M3
from nucleo import nucleo32
from util import pipe, ABIT
import raspberrypi, feather
import itertools, copy

class Mount:
    def __init__(self, position):
        self.position = position
    
    def _outline(self):
        """Return the outline of the base"""
        raise NotImplementedError
    
    def _mount(self):
        """Return the mount, positioned at the origin"""
        raise NotImplementedError

    def __call__(self):
        return translate(self.position)(self._mount())
    
    def outline(self):
        return translate(self.position)(self._outline())
    
    def __getitem__(self, i):
        return self.position[i]

    def translated(self, offset):
        x = copy.copy(self)
        x.position = util.vadd(self.position, offset)
        return x

class InsertStandoff(Mount):
    def __init__(self, position, fixing, height, insert_height=3.0):
        Mount.__init__(self, position)
        self.fixing = fixing
        self.slot_height = height
        self.insert_height = insert_height

    def _outline(self):
        return circle(r=self.fixing.insert/2.0+1.0)
    
    def _mount(self):
        return (
            pipe(h=self.slot_height, 
                 ir=self.fixing.thread/2.0, 
                 r=self.fixing.insert/2.0+1.0) +
             up(self.slot_height-self.insert_height)(
                 hole()(cylinder(d=self.fixing.insert, 
                                 h=self.insert_height))))

class Board:
    def __init__(self, dimensions, mounts, position):
        self.dimensions = dimensions
        self.mounts = list(mount.translated(position) for mount in mounts)
        self.position = position
        
    def __call__(self):
        return union()(*(mount() for mount in self.mounts))

class VerticalSlot(Mount):
    def __init__(self, position, slot_thickness, wall_thickness, slot_height, standoff_height):
        Mount.__init__(self, position)
        self.slot_thickness = slot_thickness
        self.wall_thickness = wall_thickness
        self.slot_height = slot_height
        self.standoff_height = standoff_height

    def _standoff_outline(self):
        width = 4.0
        depth = 2*self.wall_thickness + self.slot_thickness
        buttress = depth+2*self.wall_thickness
        return (
            back(buttress/2)(square([self.wall_thickness, buttress])) +
            back(depth/2)(square([width, depth])))

    def _sides_outline(self):
        return (
            self._standoff_outline() +
            hole()(back(self.slot_thickness/2)(square([4.0 + ABIT, self.slot_thickness]))))

    def _mount(self):
        depth = 2*self.wall_thickness + self.slot_thickness
        return (up(self.standoff_height)(
            linear_extrude(self.slot_height)(self._sides_outline()) +
            translate([-self.wall_thickness, -depth/2, self.slot_height/2])(
                cube([self.wall_thickness, depth, self.slot_height/2]))) +
            linear_extrude(self.standoff_height)(self._standoff_outline()))

class LeftVerticalSlot(VerticalSlot):
    def _outline(self):
        return VerticalSlot._standoff_outline(self)

class RightVerticalSlot(VerticalSlot):
    def _outline(self):
        return mirror([1,0,0])(VerticalSlot._standoff_outline(self))

    def _mount(self):
        return mirror([1,0,0])(VerticalSlot._mount(self))

class VerticalBoard(Board):
    def __init__(self, board, position, top, bottom, thickness=1.9, standoff=0.0):
        Board.__init__(
            self, 
            [board.dimensions[0], top+bottom+thickness],
            (LeftVerticalSlot([-board.dimensions[0]/2 + 0.2, 0], thickness, 1.8, board.dimensions[1]/2, standoff),
             RightVerticalSlot([board.dimensions[0]/2 + 0.2, 0], thickness, 1.8, board.dimensions[1]/2, standoff)),
            position)
        self.board = board
        self.top = top
        self.bottom = bottom
        
      
class RaspberryPiZero(Board):
    def __init__(self, position, height=3.0):
        Board.__init__(self, raspberrypi.zero.d, (InsertStandoff(p, M2_5, height + 2.0) for p in raspberrypi.zero.holes), position)

class GenericBoard(Board):
    def __init__(self, dimensions, position, holes=None, height=2.0):
        Board.__init__(
            self,
            dimensions, 
            (InsertStandoff(p, M2, height + 3.0) 
             for p in util.corners(*(holes or [d - 4.0 for d in dimensions]))),
            position)

    @staticmethod
    def b60x40(position = (0,0)):
        return GenericBoard([60.0, 40.0], position, holes=[54.0,34.0])

    @staticmethod
    def b70x30(position = (0,0)):
        return GenericBoard([70.0, 30.0], position)
    


class MiniBoard(Board):
    def __init__(self, position, height=2.0):
        Board.__init__(
            self,
            util.inch_to_mm([1.0, 1.0]),
            [InsertStandoff([0, -util.inch_to_mm(0.5) + 3.3], M3, height + 2.0)],
            position)

class Nucleo32Socket(Board):
    def __init__(self, position, height=6.0):
        Board.__init__(
            self,
            nucleo32.socket.d,
            (InsertStandoff([y,x], M2, height + 2.0) 
             for (x,y) in nucleo32.socket.screw_holes()),
            position)

class FeatherBoard(Board):
    def __init__(self, position, height=2.0):
        Board.__init__(
            self,
            feather.board.d,
            (InsertStandoff(p, M2, height + 2.0) 
             for p in feather.board.holes),
            position)


class ScrewHole(Mount):
    def __init__(self, position, fixing):
        Mount.__init__(self, position)
        self.fixing = fixing

    def _outline(self):
        return circle(r=self.fixing.thread)
    
    def _mount(self):
        return hole()(linear_extrude(2.0)(self.fixing.cut()))

class ChassisMount(Board):
    def __init__(self, chassis):
        Board.__init__(self, None, (ScrewHole(p, M2) for p in chassis.pcb_plate_mount_points()), [0,0])

class Plate:
    def __init__(self, chassis, boards):
        self.chassis_mounts = ChassisMount(chassis)
        self.boards = boards + [ self.chassis_mounts ]
        self.chassis = chassis
        
    def mounts(self):
        return itertools.chain(*(board.mounts for board in self.boards))
    
    def outline(self):
        return (hull()(*(mount.outline() for mount in self.chassis_mounts.mounts)) +
                hull()(*(mount.outline() for mount in self.mounts() if mount[0] < 0)) +
                hull()(*(mount.outline() for mount in self.mounts() if mount[0] > 0)))
    
    def assembly(self):
        return (
            linear_extrude(2.0)(self.outline()) +
            union()(*(mount() for mount in self.mounts())))

def nucleo32_feather_plate(chassis):
    nucleo32_y = -chassis.fit_forward(nucleo32.socket.d)
    feather_y = nucleo32_y + (nucleo32.socket.d[0] + feather.board.d[1])/2
    raspberrypi_y = nucleo32_y + (nucleo32.socket.d[0] + raspberrypi.zero.d[1])/2
    mini_y = feather_y + (feather.board.d[1] + util.inch_to_mm(1.0))/2 + 5
    return Plate(chassis, [
        Nucleo32Socket([0, nucleo32_y]),
        FeatherBoard([0,feather_y]),
        RaspberryPiZero([0, raspberrypi_y], height=18),
        MiniBoard([+util.inch_to_mm(0.5), mini_y]),
        MiniBoard([-util.inch_to_mm(0.5), mini_y])]).assembly()

def nano_shield_plate(chassis):
    sheild_y = 20.0
    module1_y = 7
    module2_y = 1
    raspberrypi_y = -chassis.fit_forward(raspberrypi.zero.d)
    none = lambda x: x
    cable_hole = circle(d=15.0)
    boards_bounding_y = sheild_y - module2_y + 1.9 + 4.0
    plate = Plate(chassis, [
        RaspberryPiZero([0, raspberrypi_y]),
        VerticalBoard(GenericBoard.b60x40(), [0, sheild_y], 10.0, 2.0),
        VerticalBoard(GenericBoard.b70x30(), [0, module1_y], 20.0, 2.0, standoff=10.0),
        VerticalBoard(GenericBoard.b70x30(), [0, module2_y], 20.0, 2.0, standoff=10.0)])

    reinforcement = linear_extrude(20)(intersection()(
        forward((sheild_y + module2_y)/2)(
            square([70, boards_bounding_y], center=True) -
            square([56, boards_bounding_y], center=True)) -
            back(2)(left(31+ABIT)(square([62 + 2*ABIT, module1_y + module2_y + 1 + 8]))) -
            union()(*(translate(p)(circle(d=5)) for p in chassis.pcb_plate_mount_points())),
        plate.outline()))
    return (
        plate.assembly() +
        reinforcement +
        hole()(
            linear_extrude(2.0)(
                union()(*(
                    transform(cable_hole) 
                    for transform in (none, left(20), right(20), forward(17.5), back(17.5)))))))

def export_plates(chassis):
    util.save('chassis-nano-shield-mount', nano_shield_plate(chassis))
    util.save('chassis-nucleo32-mount', nucleo32_feather_plate(chassis))

def export_scad():
    export_plates(chassis())

if __name__ == '__main__':
    export_scad()
    