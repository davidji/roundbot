from math import sqrt
from solid import *
from solid.utils import *
import util
from util import radial, pipe, ABIT
from fixings import M3

def body(height=21.0, radius=50.0, insert_height=3.0, t=2.0, arch_width=12.0):
    
    def body_cross_section():
       return translate([radius-1,0])(
            translate([1,0])(polygon(([-3, 3], [0, 6], [0, 0], [-3, 0]))) +
            translate([0, 3])(square([1, height-3])) +
            union()(*(translate([0, y])(polygon([[0,-1],[-1, 0],[0,1]])) 
                      for y in range(7, int(height), 5))) +
            translate([1, height])(polygon(([0,-3],[-3,0],[0,0]))))

    vstrut = left(1.25)(up(3)(cube([2.5,2,height-3])))
    pillar = (linear_extrude(height)(circle(d=6.0) + hole()(M3.cut())) +
              hole()(up(height - insert_height)(cylinder(d=M3.insert, h=insert_height))))
    corner = (radius - 3)/sqrt(2)
    
    class Body:
        def pillars(self):
            return radial(radius - 3, [+45, -45, +135, -135], pillar)
        
        def shell(self):
            return (rotate_extrude()(body_cross_section()) +
                    radial(radius - 3, [a + 7.5 for a in range(0,360,15)], vstrut))
        
        def body(self):
            return self.pillars() + self.shell()

        def end_module_back(self):
            return corner-12.0
        
        def end_module_bounds(self):
            return linear_extrude(height)(
                intersection()(
                    circle(r=radius),
                    (translate([-radius, corner-3, 0])(
                        square([2*radius, radius-corner+3])) +
                     translate([-radius+arch_width+t, self.end_module_back()])(
                         square([2*(radius-arch_width-t), radius - self.end_module_back()])))))

        def _mount(self, fix, position):
            return translate(position)(
                rotate([0, -90, 0])(linear_extrude(6.0)(square([height, 12.0], center=True)) + 
                                    left(height/2-M3.thread)(fix) + 
                                    right(height/2-M3.thread)(mirror([1, 0, 0])(fix))))

        def end_module_template(self):
            fix = hole()(
                down(ABIT)(linear_extrude(6.0+2*ABIT)((M3.cut()))) +
                up(t)(rotate([0,0,-90])(M3.nut.side_capture(M3.thread+ABIT))))
            mount = self._mount(fix, [radius-arch_width-t, corner-6.0, height/2])
            return intersection()(
                self.pillars(), 
                self.end_module_bounds()) + mount + mirror([1,0,0])(mount)

        def side_module_bounds(self):
            return linear_extrude(height)(
                intersection()(
                    circle(r=radius),
                    translate([radius - arch_width - t, -(corner-3.0)])(square([arch_width+t, 2*(corner-3)]))))

        def side_module_template(self):
            screw_head_r = M3.thread*1.1
            fix = hole()(
                down(ABIT)(linear_extrude(6.0+2*ABIT)((M3.cut()))) +
                linear_extrude(3.0)(circle(r=screw_head_r) + forward(screw_head_r)(square([2*screw_head_r, screw_head_r], center=True))))
            mount = self._mount(fix, [radius-arch_width-t+6.0, corner-6.0, height/2])
            return intersection()(self.side_module_bounds(), mount + mirror([0,1,0])(mount))

        def side_module_blank(self):
            return intersection()(
                self.side_module_bounds(),
                self.body() + self.side_module_template())

        def end_module_blank(self):
            return intersection()(
                self.end_module_bounds(),
                self.body() + self.end_module_template())

    return Body()


if __name__ == '__main__':
    util.save('body', body().body())    
    util.save('body-end-module-bounds', body().end_module_bounds())   
    util.save('body-side-module-bounds', body().side_module_bounds())
    util.save('body-module-bounds',
              color(Green)(body().side_module_bounds() + mirror([1,0,0])(body().side_module_bounds())) +
              color(Yellow)(body().end_module_bounds() + mirror([0,1,0])(body().end_module_bounds())))
    util.save('body-end-module-template', body().end_module_template())
    util.save('body-module-template',
              color(Green)(body().side_module_template() + mirror([1,0,0])(body().side_module_template())) +
              color(Yellow)(body().end_module_template() + mirror([0,1,0])(body().end_module_template())))
    util.save('body-end-module-blank', body().end_module_blank()())
    util.save('body-side-module-blank', body().side_module_blank()())
