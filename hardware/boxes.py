
from util import *
from fixings import M3
from solid.solidpython import linear_extrude
from honeycomb import honeycomb
from gtk.keysyms import cent

# A reminder: width = x, depth = y, left = -x, right = x, back = -y, forward = y

def builder(id, t, base_height, lid_height, lip=None, connector=None, holes=None, wells=None):
    wallt = t
    id = id + [ base_height + lid_height ]
    ed = [id[i] + 2*wallt for i in range(3)]

    center_align = translate([id[0]/2, id[1]/2])

    def connectors(x):
        return center_align(corners([ed[0]+connector.thread, ed[1]-connector.thread*4], x))

    def outline():
        o = translate([-wallt]*2)(square(ed[0:2]))
        if connector:
            o = o + connectors(circle(r=connector.thread+1))
        return o

    def bounds(z, height):
        return up(z)(linear_extrude(height)(outline()))
    
    box_bounds = bounds(-base_height-wallt, ed[2])
    box = box_bounds - down(base_height)(cube(id))
    
    if connector:
        head_height=connector.thread/1.25
        box = box + down(base_height+wallt)(
            connectors(
                pipe(ir=connector.thread/2, r=connector.thread+1, h=ed[2]) +
                hole()(up(ed[2]-head_height)(cylinder(h=head_height+ABIT, r=connector.thread)) +
                       connector.nut.capture())))

    def cutout(profile):
        return rotate([0, -90, 0])(down(ABIT)(linear_extrude(height=wallt+2*ABIT)(profile)))

    class Builder:
        def __init__(self, box, bounds):
            self.box = box
            self.bounds = bounds
        
        def right(self, profile, center=False):
            return Builder(self.box - 
                       translate([center and id[0]/2 or 0, id[1] + wallt, 0])(
                           rotate(90)(cutout(profile))),
                        self.bounds)
        
        def front(self, profile, center=False):
            return Top(self.box - translate([0, center and id[1]/2 or 0, 0])(
                cutout(profile)),
                self.bounds)
        
        def well(self, wells, t=1.0, flange=wallt):
            return Builder(
                self.box +
                up(lid_height)(linear_extrude(height=wallt)(offset(delta=flange)(wells))) +
                linear_extrude(height=lid_height)(offset(delta=t)(wells)) +
                hole()(linear_extrude(height=lid_height+wallt)(wells)),
                self.bounds)

        def hole(self, holes, flange=wallt):
            return Builder(self.box + up(lid_height)(
                linear_extrude(height=wallt)(offset(delta=flange)(holes)) +
                hole()(linear_extrude(height=wallt)(holes))),
                self.bounds)
        
        def lidVent(self, vent):
            return Builder(self.box -
                           translate([id[0]/2, id[1]/2, lid_height-ABIT])(
                               linear_extrude(height=wallt+2*ABIT)(
                                   honeycomb(2.0, 1.0, vent[0], vent[1], center=True, inverted=True))),
                           self.bounds)
            
        def build(self, center=False):
            bounded = intersection()(self.box, self.bounds)
            return center and translate([-id[0]/2, -id[1]/2, 0])(bounded) or bounded
        
        def lid(self):
            return Builder(self.box, bounds(0, lid_height+wallt))
        
        def base(self):
            return Builder(self.box, bounds(-base_height-wallt, base_height+wallt))

    return Builder(box, bounds)
            

def bottom(*args, **kwargs):
    return builder(*args, **kwargs).bottom()
    
def top(id, t, center=False, vent=None, lip=None, connector=None, holes=None, wells=None):
    box = bottom(id, t, center, vent, lip, connector, True)
    return box
