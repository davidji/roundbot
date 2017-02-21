
from util import *
from fixings import M3
from solid.solidpython import linear_extrude
from honeycomb import honeycomb
from gtk.keysyms import cent

# A reminder: width = x, depth = y, left = -x, right = x, back = -y, forward = y

def mirror_corners(width, depth):
    def f(obj):
        corner = translate([-width/2, -depth/2])(obj)
        left = corner + mirror([0, 1])(corner)
        right = mirror([1, 0])(left)
        return (left + right)
    return f

def builder(id, t, base_height, lid_height):
    wallt = t
    id = id + [ base_height + lid_height ]
    ed = [id[i] + 2*wallt for i in range(3)]

    center_align = translate([id[0]/2, id[1]/2])
    floor = -base_height-wallt

    def connector_body(connector):
        return intersection()(
            hull()(
                circle(r=connector.thread*1.3) + 
                translate([connector.thread/2, -connector.thread*2])(
                    square([wallt, connector.thread*4]))),
            translate([-connector.thread*1.3, -connector.thread*2])(
                square([wallt+connector.thread*1.8, connector.thread*4])))
        
    def extrude_bounds(outline, z = floor, height = ed[2]):
        return up(z)(linear_extrude(height)(outline))
    
    simple_outline = translate([-wallt]*2)(square(ed[0:2]))
    bounds = (simple_outline, floor, ed[2])
    
    box = extrude_bounds(*bounds) - down(base_height)(cube(id))
    
    def connector_insets(connector, internal=True):
        screw_head_r = connector.thread*1.3

        def head():
            if internal:
                return circle(r=screw_head_r)
            else:
                return hull()(
                    circle(r=screw_head_r) +
                    translate([-wallt-connector.thread/2, -connector.thread*2])(
                        square([wallt, connector.thread*4])))
        
        screw_head_depth = connector.thread*0.6
        screw_head_height = lid_height+wallt-screw_head_depth
        return hole()(up(screw_head_height)(
            linear_extrude(screw_head_depth+ABIT)(head())) +    
            down(base_height+wallt)(connector.nut.capture()))
    
    def connector_bulkheads(connector):
        height = connector.nut.h*1.5
        bulkhead = cylinder(r=connector.thread+1, h=height)
        return down(base_height+wallt)(bulkhead) + up(lid_height + wallt - height)(bulkhead)
    
    def cutout(profile, thickness=None):
        return rotate([0, -90, 0])(down(ABIT)(linear_extrude(height=(thickness and wallt - thickness or wallt+ABIT) + ABIT)(profile)))

    class Builder:
        def __init__(self, box, bounds):
            self.box = box
            self.bounds = bounds

        def screw_together(self, fixing):
            def connectors(x):
                return center_align(mirror_corners(ed[0]+fixing.thread, ed[1]-fixing.thread*4)(x))

            tabs = connectors(connector_body(fixing))
            (outline, z, h) = self.bounds
            return Builder(
                self.box +
                extrude_bounds(tabs) +
                connectors(
                   up(floor)(
                       pipe(ir=fixing.thread/2, r=fixing.thread+1, h=ed[2])) +
                   connector_insets(fixing, internal=False)),
                (outline + tabs, z, h))
        
        def right(self, profile, thickness=None, center=False):
            def position(o):
                return translate([center and id[0]/2 or 0, id[1] + wallt, 0])(rotate(90)(o))

            return Builder(self.box - position(cutout(profile, thickness)), self.bounds)
        
        def front(self, profile, center=False, thickness=None):
            return Builder(self.box - translate([thickness and -thickness-ABIT or 0, center and id[1]/2 or 0, 0])(
                cutout(profile, thickness)),
                self.bounds)
        
        def stacking(self, wells, wall_thickness = 1.0, height=None, thickness = 1.6):
            height = height or base_height - thickness
            walls = offset(delta=t)(wells)
            return Builder(
                self.box +
                down(base_height)(linear_extrude(height)(walls)) + 
                linear_extrude(lid_height)(walls) +
                hole()(up(floor)(linear_extrude(height+wallt)(wells)) + 
                                 linear_extrude(lid_height+wallt)(wells)),
                self.bounds)
            
        def well(self, wells, t=1.0, flange=wallt):
            return Builder(
                self.box +
                up(lid_height)(linear_extrude(height=wallt)(offset(delta=flange)(wells))) +
                    up(ABIT)(linear_extrude(height=lid_height-ABIT)(offset(delta=t)(wells))) +
                    hole()(linear_extrude(height=lid_height+wallt)(wells)),
                self.bounds)

        def hole(self, holes, flange=wallt):
            return Builder(self.box + up(lid_height)(
                linear_extrude(height=wallt)(offset(delta=flange)(holes)) +
                hole()(linear_extrude(height=wallt)(holes))),
                self.bounds)
        
        def lidVent(self, vent):
            vent = translate([id[0] / 2, id[1] / 2, lid_height - ABIT])(
                linear_extrude(height=wallt + 2 * ABIT)(
                    honeycomb(2.0, 1.0, vent[0], vent[1], center=True, inverted=True)))
            return Builder(self.box - vent, self.bounds)
        
        def pinch_mounts(self, shape, positions, height = None, thickness = 1.6):
            height = height or base_height - thickness
            mount = down(base_height)(
                linear_extrude(height)(shape) +
                up(height+thickness+ABIT)(linear_extrude(id[2] - height - thickness - ABIT)(shape)))
            return Builder(self.box + union()(*(translate(position)(mount) for position in positions)), self.bounds)

        
        def pillar_mounts(self, connector, positions, height = None, thickness = 1.6):
            """This is for PCBs that have through holes. On the base,
            there is a standoff, with a pin, which goes through the hole,
            from the top there's a holding pin, which holds the board
            on the pin."""
            height = height or base_height - thickness
            mount = down(base_height)(
                cylinder(r=connector.thread, h=height) +
                cylinder(d=connector.thread, h=height + thickness - 0.5) +
                up(height+thickness+ABIT)(cylinder(r=connector.thread, h=id[2] - height - thickness - ABIT)))
            return Builder(self.box + union()(*(translate(position)(mount) for position in positions)), self.bounds)
        
        def screw_mounts(self, connector, positions, height = None, thickness = 1.6):
            """This is similar to mount, but uses an actual fixing, which
            holds the PCB in place, but also goes right through the box,
            and holds the box together. There's an inset for the screw
            on the top, and a nut capture in the base."""
            height = height or (base_height - thickness)
            
            mount = (down(base_height)(
                        down(wallt)(
                            pipe(ir=connector.thread/2, r=connector.thread, h=height+wallt)) +
                        up(height+thickness+ABIT)(
                            pipe(ir=connector.thread/2, 
                                 r=connector.thread, 
                                 h=((id[2] + wallt) - (height + thickness + ABIT))))) +
                     connector_bulkheads(connector) +
                     connector_insets(connector))
            return Builder(self.box + union()(*(translate(position)(mount) for position in positions)), self.bounds)
        
        def build(self, center=False):
            bounded = intersection()(self.box, extrude_bounds(*self.bounds))
            return center and translate([-id[0]/2, -id[1]/2, 0])(bounded) or bounded
        
        def lid(self):
            (outline,_,_) = self.bounds
            return Builder(self.box, (outline, 0, lid_height+wallt))
        
        def base(self):
            (outline,_,_) = self.bounds
            return Builder(self.box, (outline, floor, -floor))
        
        def spacer(self):
            """Make a spacer, which is the base walls, and connecting tabs.
            It also includes stand offs, which only makes sense if they
            touch the walls"""
            (outline,_,_) = self.bounds
            return Builder(self.box, (outline, -base_height, base_height))
            
        
    return Builder(box, bounds)
            

def bottom(*args, **kwargs):
    return builder(*args, **kwargs).bottom()
    
def top(id, t, center=False, vent=None, lip=None, connector=None, holes=None, wells=None):
    box = bottom(id, t, center, vent, lip, connector, True)
    return box
