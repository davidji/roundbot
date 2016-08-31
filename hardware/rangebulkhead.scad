$fa = 0.1; $fs = 0.5;

difference(){
	intersection() {
		linear_extrude(height = 25.0000000000) {
			difference() {
				difference() {
					difference() {
						circle(r = 50.0000000000);
						rotate(a = -90) {
							translate(v = [0, -50.0000000000, 0]) {
								square(center = true, size = [150.0000000000, 100.0000000000]);
							}
						}
						rotate(a = -90) {
							translate(v = [0, -50.0000000000, 0]) {
								square(center = true, size = [150.0000000000, 100.0000000000]);
							}
						}
					}
					union() {
						square(center = true, size = [65, 56, 10]);
						square(center = true, size = [70.0000000000, 50.0000000000]);
					}
				}
				square(center = true, size = [35.0000000000, 100.0000000000]);
			}
		}
		union() {
			union() {
				union() {
					linear_extrude(height = 25.0000000000) {
						difference() {
							union() {
								union() {
									difference() {
										difference() {
											circle(r = 50.0000000000);
											rotate(a = -90) {
												translate(v = [0, -50.0000000000, 0]) {
													square(center = true, size = [150.0000000000, 100.0000000000]);
												}
											}
											rotate(a = -90) {
												translate(v = [0, -50.0000000000, 0]) {
													square(center = true, size = [150.0000000000, 100.0000000000]);
												}
											}
										}
										difference() {
											circle(r = 47.0000000000);
											rotate(a = -90) {
												translate(v = [0, -47.0000000000, 0]) {
													square(center = true, size = [141.0000000000, 94.0000000000]);
												}
											}
											rotate(a = -90) {
												translate(v = [0, -47.0000000000, 0]) {
													square(center = true, size = [141.0000000000, 94.0000000000]);
												}
											}
										}
									}
									translate(v = [42.5000000000, 0, 0]) {
										square(center = true, size = [3, 100.0000000000]);
									}
								}
								union() {
									rotate(a = -45) {
										translate(v = [0, 47.0000000000, 0]) {
											difference() {
												circle(r = 3);
											}
										}
									}
									rotate(a = -135) {
										translate(v = [0, 47.0000000000, 0]) {
											difference() {
												circle(r = 3);
											}
										}
									}
								}
							}
							union() {
								rotate(a = -90) {
									translate(v = [0, 35.0000000000, 0]) {
										circle(d = 15);
									}
								}
							}
						}
					}
					translate(v = [41.0000000000, 0, 12.5000000000]) {
						rotate(a = [0, 90, 0]) {
							linear_extrude(height = 10) {
								difference() {
									offset(chamfer = false, r = 1.8000000000) {
										union() {
											rotate(a = 0) {
												translate(v = [0, 13.0000000000, 0]) {
													circle(r = 8.1000000000);
												}
											}
											rotate(a = 180) {
												translate(v = [0, 13.0000000000, 0]) {
													circle(r = 8.1000000000);
												}
											}
										}
									}
								}
							}
						}
					}
				}
				translate(v = [17.5000000000, 0, 12.5000000000]) {
					rotate(a = [0, 90, 0]) {
						linear_extrude(height = 3) {
							difference() {
								square(center = true, size = [25.0000000000, 100.0000000000]);
								translate(v = [-3, 0, 0]) {
									union() {
										union() {
											translate(v = [-6.0000000000, 40.0000000000]) {
												circle(r = 1.5750000000);
											}
											translate(v = [6.0000000000, 40.0000000000]) {
												circle(r = 1.5750000000);
											}
											translate(v = [6.0000000000, -40.0000000000]) {
												circle(r = 1.5750000000);
											}
											translate(v = [-6.0000000000, -40.0000000000]) {
												circle(r = 1.5750000000);
											}
										}
										union() {
											translate(v = [-6.0000000000, 30.0000000000]) {
												circle(r = 1.5750000000);
											}
											translate(v = [6.0000000000, 30.0000000000]) {
												circle(r = 1.5750000000);
											}
											translate(v = [6.0000000000, -30.0000000000]) {
												circle(r = 1.5750000000);
											}
											translate(v = [-6.0000000000, -30.0000000000]) {
												circle(r = 1.5750000000);
											}
										}
									}
								}
							}
						}
					}
				}
			}
			linear_extrude(height = 3) {
				difference() {
					difference() {
						difference() {
							circle(r = 50.0000000000);
							rotate(a = -90) {
								translate(v = [0, -50.0000000000, 0]) {
									square(center = true, size = [150.0000000000, 100.0000000000]);
								}
							}
							rotate(a = -90) {
								translate(v = [0, -50.0000000000, 0]) {
									square(center = true, size = [150.0000000000, 100.0000000000]);
								}
							}
						}
						union() {
							rotate(a = -90) {
								translate(v = [0, 35.0000000000, 0]) {
									circle(d = 15);
								}
							}
						}
					}
					union() {
						rotate(a = -45) {
							translate(v = [0, 47.0000000000, 0]) {
								circle(r = 1.5750000000);
							}
						}
						rotate(a = -135) {
							translate(v = [0, 47.0000000000, 0]) {
								circle(r = 1.5750000000);
							}
						}
					}
				}
			}
		}
	}
	/* Holes Below*/
	intersection(){
		union(){
			union(){
				union(){
					linear_extrude(height = 25.0000000000){
						union(){
							union(){
								union(){
									rotate(a = -45){
										translate(v = [0, 47.0000000000, 0]){
											union(){
												circle(r = 1.5750000000);
											}
										}
									}
									rotate(a = -135){
										translate(v = [0, 47.0000000000, 0]){
											union(){
												circle(r = 1.5750000000);
											}
										}
									}
								}
							}
						}
					}
					translate(v = [41.0000000000, 0, 12.5000000000]){
						rotate(a = [0, 90, 0]){
							linear_extrude(height = 10){
								difference(){
									union() {
										rotate(a = 0) {
											translate(v = [0, 13.0000000000, 0]) {
												circle(r = 8.1000000000);
											}
										}
										rotate(a = 180) {
											translate(v = [0, 13.0000000000, 0]) {
												circle(r = 8.1000000000);
											}
										}
									}
								}
							}
						}
					}
				}
			}
		}
	} /* End Holes */ 
}
/***********************************************
*********      SolidPython code:      **********
************************************************
 
from __future__ import division

import os, sys

from solid import *
from solid.utils import *
from fixings import M3, M2
from util import *

from sensors import hc_sr04
from raspberrypi import aplus

import lego

FA=0.1
FS=0.5

def bulkhead(radius=50.0, height=25.0, arch_length=35.0):
    range_depth = 9.0
    range_x = radius - range_depth

    arch_cut = square([arch_length, radius*2], center=True)
    electronics = (square(aplus.d, center=True) + square([70.0, 50.0], center=True))
    def bounds():
        return linear_extrude(height=height)(arc(radius, -90, +90) - electronics - arch_cut)

    def rangesensor():
        return translate([range_x, 0, height/2])(
            rotate([0, 90, 0])(
                linear_extrude(height=10)(
                    offset(1.8)(hc_sr04.tranceiver_cut()) -
                    hole()(hc_sr04.tranceiver_cut()))))

    def flange():
        def position(x):
            return translate([arch_length/2, 0, height/2])(rotate([0,90,0])(x))
        section = (square([height, 2*radius], center=True) -
                   left(3)(corners([height-13, 2*(radius-10)], M3.cut()) +
                           corners([height-13, 2*(radius-20)], M3.cut())))
        return position(linear_extrude(height=3)(section))

    def tall_profile():
        return ((arc(radius, -90, +90) - arc(radius-3, -90, +90)) +
                right(range_x + 1.5)(square([3, radius*2], center=True)) +
                radial(radius-3, [ -45, -135 ], circle(r=3) - hole()(M3.cut())) -
                radial(radius - 15, [-90], circle(d=15)))

    return intersection()(
        bounds(),
        (linear_extrude(height=height)(tall_profile()) + 
         rangesensor() +
         flange() +
         linear_extrude(height=3)(
             arc(radius, -90, +90) -
             radial(radius - 15, [-90], circle(d=15)) -
             radial(radius - 3, [ -45, -135 ], M3.cut()))))

def assembly():
    return bulkhead()

if __name__ == '__main__':
    out_dir = sys.argv[1] if len(sys.argv) > 1 else os.curdir
    file_out = os.path.join( out_dir, 'rangebulkhead.scad')
 
    a = assembly()
    print("%(__file__)s: SCAD file written to: \n%(file_out)s"%vars())
    scad_render_to_file( a, file_out, file_header='$fa = %s; $fs = %s;' % (FA, FS), include_orig_code=True)
 
 
************************************************/
