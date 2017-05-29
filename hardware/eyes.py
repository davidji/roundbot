
from solid import *
from solid.utils import *
import util
import body
from util import tube, pipe, ABIT, corners, vadd
from fixings import M2, M3
import raspberrypi
from solid.solidpython import linear_extrude

class oled:
    d = [27.0, 28.0, 5.0]
    
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
            return center and util.origin([-x for x in center]) or util.origin(corner)
        
        @staticmethod
        def fixings(center=False):
            o = [-x for x in center and oled.display.center or corner]
            return util.origin(o)(*oled.fixings())
        

def eye(w=35.0, h=10.0, t=2.0, insert_depth=3.2):
    r = h/2 + w*w/(8*h)
    return (
        down(h)(
            intersection()(
                cylinder(d=w, h=h),
                up(r)(sphere(r = r + t))) +
            linear_extrude(h)(offset(delta=t)(square(oled.display.d, center=True)))+
            union()(*[translate(p)(
                down(1.8)(linear_extrude(h-t+1.8)(circle(r=M2.thread) + hole()(M2.cut()))))
                      for p in oled.display.fixings(center=True)]) +
            hole()(up(r)(intersection()(cylinder(d=w, h=2*r, center=True), sphere(r=r)))) +
            hole()(linear_extrude(2*h, center=True)(square(oled.display.d, center=True))) +
            down(oled.d[2])(hole()(
                linear_extrude(oled.d[2])(
                    translate([-x for x in oled.display.center])(
                        offset(r=0.5)(square(oled.d[0:2]))))))))

def eyes(r=50.0, l=70.0, t=2.0, insert_depth=3.2, arch_width=12.0):
    spacing = r/sqrt(2.0)
    eyewidth = 0.8*spacing
    eyeforward = r/sqrt(2.0)
    eyedepth = r - eyeforward
    socketdepth = 10.0
    eyeback = eyeforward - socketdepth
    depth = eyedepth + socketdepth
    d = eyewidth + 2*t

    def eyesposition(a):
        return translate([0, eyeforward, d/2])(rotate([-90, 0, 0])(a))
    def eyepositions(a):
        b = eyesposition(a)
        return left(spacing/2)(b) + right(spacing/2)(b)

    eyesbody = body.body(radius=r, height=d)
    # skull = tube(r=r, t=t, h=d)
    eyesection = (square([spacing, eyewidth], center=True) + 
                  left(spacing/2)(circle(d=eyewidth)) +
                  right(spacing/2)(circle(d=eyewidth)))
    socketshell = eyesbody.end_module_bounds()
    socket = (eyesposition(linear_extrude(eyedepth)(eyesection)) +
              eyepositions(down(t)(cylinder(d=eyewidth, h=eyedepth+t))))
    backfixing = hole()(
                down(ABIT)(linear_extrude(6.0+2*ABIT)((M3.cut()))) +
                up(t)(M3.nut.side_capture(M3.thread+ABIT)))
    backfixings = translate([0, eyesbody.end_module_back(), d/2])(rotate([-90, 0, 0])(
        forward(d/2-M3.thread)(rotate([0,0,180])(backfixing)) +
        back(d/2 - M3.thread)(backfixing)))

    class Eyes:
        def eyes(self):
            return intersection()(
                eyesbody.end_module_bounds(),
                eyesbody.end_module_template() +
                socketshell -
                socket +
                eyepositions(eye(w=eyewidth, h=socketdepth, t=t)) +
                backfixings)
            
        def cradle(self):
            return linear_extrude(height=d*1.2)(
                translate([-r, eyeback])(
                    square([2*r, depth+2*t])) - 
                circle(r=r))
    return Eyes()

if __name__ == '__main__':
    util.save('eye', eye())    
    util.save('eyes', eyes().eyes())
    util.save('eyes-cradle', eyes().cradle())
