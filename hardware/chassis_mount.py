
from solid import *
from solid.utils import *
import util
from chassis import chassis
from fixings import M2, M2_5, M3
from nucleo import nucleo32
from util import tube
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
        self.height = height
        self.insert_height = insert_height

    def _outline(self):
        return circle(r=self.fixing.insert/2.0+1.0)
    
    def _mount(self):
        return (
            tube(h=self.height, 
                 ir=self.fixing.thread/2.0, 
                 r=self.fixing.insert/2.0+1.0) +
             up(self.height-self.insert_height)(
                 hole()(cylinder(d=self.fixing.insert, 
                                 h=self.insert_height))))

class Board:
    def __init__(self, dimensions, mounts, position):
        self.dimensions = dimensions
        self.mounts = list(mount.translated(position) for mount in mounts)
        self.position = position
        
    def __call__(self):
        return union()(*(mount() for mount in self.mounts))

class RaspberryPiZero(Board):
    def __init__(self, position, height=2.0):
        Board.__init__(self, raspberrypi.zero.d, (InsertStandoff(p, M2_5, height + 2.0) for p in raspberrypi.zero.holes), position)

class GenericBoard(Board):
    def __init__(self, dimensions, position, height=2.0):
        Board.__init__(
            self,
            dimensions, 
            (InsertStandoff(p, M2, height + 2.0) 
             for p in util.corners([d - 4.0 for d in dimensions])))

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
            (InsertStandoff(p, M3, height + 2.0) 
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
    
    def assembly(self):
        for mount in self.mounts():
            print mount()
        return (
            linear_extrude(2.0)(
                hull()(*(mount.outline() for mount in self.chassis_mounts.mounts)) +
                hull()(*(mount.outline() for mount in self.mounts() if mount[0] < 0)) +
                hull()(*(mount.outline() for mount in self.mounts() if mount[0] > 0))) +
            union()(*(mount() for mount in self.mounts())))

def export_plates(chassis):
    util.save('chassis-nucleo32-mount', Plate(chassis, [
        RaspberryPiZero([0, 0], height=14.0),
        FeatherBoard([0,0]),
        MiniBoard([0, raspberrypi.zero.d[1]/2 + util.inch_to_mm(0.5)]),
        MiniBoard([+18, raspberrypi.zero.d[1]/2 + util.inch_to_mm(0.5)]),
        MiniBoard([-18, raspberrypi.zero.d[1]/2 + util.inch_to_mm(0.5)]),
        Nucleo32Socket([0, -chassis.fit_forward(nucleo32.socket.d)])]).assembly())

def export_scad():
    export_plates(chassis())

if __name__ == '__main__':
    export_scad()
    