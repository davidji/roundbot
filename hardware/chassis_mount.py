
from solid import *
from solid.utils import *
import util
from chassis import chassis
from fixings import M2, M2_5, M3
from nucleo import nucleo32
from util import pipe
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
            pipe(h=self.height, 
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
             for p in util.corners(*[d - 4.0 for d in dimensions])),
            position)

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
    
    def assembly(self):
        return (
            linear_extrude(2.0)(
                hull()(*(mount.outline() for mount in self.chassis_mounts.mounts)) +
                hull()(*(mount.outline() for mount in self.mounts() if mount[0] < 0)) +
                hull()(*(mount.outline() for mount in self.mounts() if mount[0] > 0))) +
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
    sheild_y = chassis.fit_forward([60.0,40.0])
    print sheild_y
    return Plate(chassis, [
        GenericBoard([60.0, 40.0], [0, sheild_y]),
        GenericBoard([60.0, 40.0], [0, -sheild_y])]).assembly()

def export_plates(chassis):
    util.save('chassis-nano-shield-mount', nano_shield_plate(chassis))
    util.save('chassis-nucleo32-mount', nucleo32_feather_plate(chassis))

def export_scad():
    export_plates(chassis())

if __name__ == '__main__':
    export_scad()
    