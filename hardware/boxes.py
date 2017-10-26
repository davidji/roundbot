
import util
from util import *
from fixings import M3
from solid import linear_extrude
from solid.utils import *
from honeycomb import honeycomb
from __builtin__ import staticmethod, setattr

# A reminder: width = x, depth = y, left = -x, right = x, back = -y, forward = y

def mirror_corners(width, depth):
    def f(obj):
        corner = translate([-width/2, -depth/2])(obj)
        left = corner + mirror([0, 1])(corner)
        right = mirror([1, 0])(left)
        return (left + right)
    return f


class Projection:
    def __init__(self, name, translate, rotate, axes):
        self.name = name
        self.translate = translate
        self.rotate = rotate
        self.axes = axes

    def transform(self, id):
        def transform(x):
            return translate([ float(a*b)/2 for (a, b) in zip(self.translate, id)])(rotate(self.rotate)(x))
        return transform

class Face:
    def __init__(self, projection, box):
        self.projection = projection
        self.box = box

    def __call__(self):
        return self.projection.transform(self.box.id)

    def dimensions(self):
        return [ self.box.id[axis] for axis in self.projection.axes]

    def blank(self):
        return linear_extrude(self.box.t)(
            square([d + 2*self.box.t for d in self.dimensions()], center=True))

class Box:       
    top =    Projection("top",    UP_VEC,      (0, 0, 0),    (X, Y))
    bottom = Projection("bottom", DOWN_VEC,    (180, 0, 0),  (X, Y))
    left =   Projection("left",   LEFT_VEC,    (90, 0, 270), (Y, Z))
    right =  Projection("right",  RIGHT_VEC,   (90, 0, 90),  (Y, Z))
    front =  Projection("front",  FORWARD_VEC, (90, 0, 180), (X, Z))
    back =   Projection("back",   BACK_VEC,    (90, 0, 0),   (X, Z))

    projections = (top, bottom, left, right, front, back)

    def __init__(self, id, t):
        self.id = id
        self.t = t
        self.faces = {}
        for p in Box.projections:
            face = Face(p, self)
            self.faces[p.name] = face
            setattr(self, p.name, face)

    def hole(self):
        def h(x):
            return hole()(down(ABIT)(linear_extrude(self.t + 2*ABIT)(x)))
        return h

    def assemble(self, **faces):
        return union()(*(self.faces[key]()(value) for (key, value) in faces.items()))

    def above(self, height, top, bottom, **sides):
        return (
            self.top()(top) + 
            intersection()(
                up((self.id[2] - height)/2)(cube([self.id[0]+2*self.t, self.id[1]+2*self.t, height], center=True)),
                union()(*(self.faces[key]()(value) for (key, value) in sides.items()))))

    def below(self, height, top, bottom, **sides):
        return (
            self.bottom()(bottom) +
            intersection()(
                down((self.id[2] - height)/2)(cube([self.id[0]+2*self.t, self.id[1]+2*self.t, height], center=True)),
                union()(*(self.faces[key]()(value) for (key, value) in sides.items()))))

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
        
        def left(self, profile, thickness=None, center=False):
            def position(o):
                return translate([center and -id[0]/2 or -id[0], id[1] + wallt, 0])(rotate([0, 0, -90])(o))
            return Builder(self.box - position(cutout(profile, thickness)), self.bounds)

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

def roundsquare(d, r):
    w, d, h = d
    return linear_extrude(h, center=True)(hull()(*(translate(p)(circle(r=r)) for p in corners(w,d))))

def roundcube(d, r):
    w, d, h = d
    return (union()(*(translate(p)(sphere(r=r)) for p in corners(w,d,h))) +
            roundsquare([w, d, h], r) +
            rotate([0, 90, 0])(roundsquare([h, d, w], r)) +
            rotate([90, 0, 0])(roundsquare([w, h, d], r)))

def roundbox(d, r, t):
    return roundcube(d, r) - roundcube(d, r-t)

DIVIDER_INTERLOCK = 1.0

def organiser_divider(d, t=1.5, ri=5.0, ro=None):
    ro = ro or ri+t
    tubd = [(d[0]-3*t)/2.0-2*ri, d[1]-2*(ri+t), d[2]]
    tub = hole()(up(ri + t)(roundcube(tubd, ri)))
    return (roundsquare([d[0]-2*ro, d[1]-2*ro, d[2]], ro) + 
            left(d[0]/4.0-t/2.0)(tub) + 
            right(d[0]/4.0)(tub))

ORGANIZER_DEPTH = 36.0

def export_scad():
    util.save('roundcube', roundcube([30.0,20.0,10.0], 3))
    util.save('roundbox', intersection()(
        linear_extrude(13.0)(square([36.0, 26.0], center=True)),
        roundbox([30.0,20.0,10.0], 3, 2)))
    util.save('organiser-divider-4x3', organiser_divider([64.5, 50.0, 36/2]))
    util.save('organiser-divider-5x4-2layers', organiser_divider([54.0, 41.0, ORGANIZER_DEPTH/3]))
    util.save('organiser-divider-5x4-3layers', organiser_divider([54.0, 41.0, ORGANIZER_DEPTH/3]))

if __name__ == '__main__':
    export_scad()
