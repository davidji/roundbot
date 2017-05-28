
from solid import *
from solid.utils import *
import util
import body
from util import tube, pipe, ABIT, corners, vadd
from fixings import M2, M3
import raspberrypi

class oled:
    d = [27.0, 28.0]
    
    # Fixings are M2
    fixing = M2
    # square arrangement [23, 23]
    @staticmethod
    def fixings(center=False):
        return (center and corners(23.0, 23.0, center=True)
                or util.origin([2.0, 2.5])(*corners(23.0, 23.0, center=False)))

    class display:
        d = [26.0, 15.0]
        corner = [0.5, 5.0]
        center = vadd(corner, [x/2 for x in d])
        
        @staticmethod
        def origin(center=False):
            return center and util.origin([-x for x in oled.display.center]) or util.origin(corner)
        
        @staticmethod
        def fixings(center=False):
            o = [-x for x in center and oled.display.center or corner]
            return util.origin(o)(*oled.fixings())
        

def eye(w=35.0, h=10.0, t=2.0, fixing=M3):
    r = h/2 + w*w/(8*h)
    return (
        down(h)(
            intersection()(
                cylinder(d=w, h=h),
                up(r)(sphere(r = r + t))) +
            linear_extrude(h)(offset(delta=t)(square(oled.display.d, center=True)))+
            union()(*[translate(p)(tube(r=oled.fixing.thread, ir=oled.fixing.thread/2, h=h-t) +
                                   hole()(cylinder(d=oled.fixing.insert, h=3.0))) for p in oled.display.fixings(center=True)]) -
            up(r)(sphere(r=r)) +
            hole()(linear_extrude(2*h, center=True)(square(oled.display.d, center=True)))))

def head1(l=70.0, d=50.0, t=2.0):
    eye = translate([d/2 - 10.0, 0, d/2 - l/4])(rotate([0, 90, 0])(
        eyesocket(w=l/2, t=t)))
    skull = rotate([90, 0, 0])(tube(r=d/2, t=2, h=70.0, center=True))
    return forward(l/4)(eye) + skull + back(l/4)(eye)

def head2(r=50.0, l=70.0, t=2.0):
    spacing = r/sqrt(2.0)
    w = 0.8*spacing
    eyeforward = r/sqrt(2.0)
    eyedepth = r - eyeforward
    d = w + 2*t

    def eyesposition(a):
        return translate([0, eyeforward, d/2])(rotate([-90, 0, 0])(a))
    def eyepositions(a):
        b = eyesposition(a)
        return left(spacing/2)(b) + right(spacing/2)(b)

    skull = body.body(radius=r, height=d)
    # skull = tube(r=r, t=t, h=d)
    eyesection = (square([spacing, w], center=True) + 
                  left(spacing/2)(circle(d=w)) +
                  right(spacing/2)(circle(d=w)))
    socketshell = eyesposition(down(t)(linear_extrude(eyedepth+t)(square([spacing+w+2*t, w+2*t], center=True))))
    pistandoffs = eyesposition(down(20)(
        linear_extrude(20)(square([raspberrypi.zero.d[0]+2*2*raspberrypi.zero.fixing.thread, d], center=True) -
                           square([raspberrypi.zero.d[0], d], center=True)) -
        union()(
        *[translate(p)(cylinder(d=raspberrypi.zero.fixing.insert, h=3.0) + cylinder(d=raspberrypi.zero.fixing.thread, h=20.0))
          for p in util.corners(raspberrypi.zero.d[0]+2*raspberrypi.zero.fixing.thread, raspberrypi.zero.h[1])])))
    socket = (eyesposition(linear_extrude(eyedepth)(eyesection)) +
              eyepositions(down(t)(cylinder(d=w, h=eyedepth+t))))
    return intersection()(
        cylinder(r=r, h=w+2*t),
        skull +
        socketshell +
        pistandoffs -
        socket +
        eyepositions(eye(w=w, t=t)))

if __name__ == '__main__':
    util.save('eye', eye())    
    util.save('head', head2())