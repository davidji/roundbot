$fa = 0.1; $fs = 0.5;

union() {
	union() {
		difference() {
			difference() {
				linear_extrude(height = 50.0000000000) {
					union() {
						difference() {
							difference() {
								difference() {
									difference() {
										difference() {
											circle(r = 50.0000000000);
											rotate(a = -60) {
												translate(v = [0, -50.0000000000, 0]) {
													square(center = true, size = [150.0000000000, 100.0000000000]);
												}
											}
											rotate(a = -120) {
												translate(v = [0, -50.0000000000, 0]) {
													square(center = true, size = [150.0000000000, 100.0000000000]);
												}
											}
										}
										difference() {
											circle(r = 47.0000000000);
											rotate(a = -60) {
												translate(v = [0, -47.0000000000, 0]) {
													square(center = true, size = [141.0000000000, 94.0000000000]);
												}
											}
											rotate(a = -220) {
												translate(v = [0, -47.0000000000, 0]) {
													square(center = true, size = [141.0000000000, 94.0000000000]);
												}
											}
										}
									}
									difference() {
										circle(r = 47.0000000000);
										rotate(a = 40) {
											translate(v = [0, -47.0000000000, 0]) {
												square(center = true, size = [141.0000000000, 94.0000000000]);
											}
										}
										rotate(a = -120) {
											translate(v = [0, -47.0000000000, 0]) {
												square(center = true, size = [141.0000000000, 94.0000000000]);
											}
										}
									}
								}
								union() {
									rotate(a = -45) {
										translate(v = [0, 47.0000000000, 0]) {
											union() {
												circle(r = 3);
												translate(v = [0, 1.5000000000, 0]) {
													square(center = true, size = [6, 3]);
												}
											}
										}
									}
									rotate(a = -135) {
										translate(v = [0, 47.0000000000, 0]) {
											union() {
												circle(r = 3);
												translate(v = [0, 1.5000000000, 0]) {
													square(center = true, size = [6, 3]);
												}
											}
										}
									}
								}
							}
							square(center = true, size = [70, 56]);
						}
						union() {
							rotate(a = -45) {
								translate(v = [0, 47.0000000000, 0]) {
									difference() {
										difference() {
											circle(r = 6);
											rotate(a = 180) {
												translate(v = [0, -6, 0]) {
													square(center = true, size = [18, 12]);
												}
											}
											rotate(a = -180) {
												translate(v = [0, -6, 0]) {
													square(center = true, size = [18, 12]);
												}
											}
										}
										difference() {
											circle(r = 3);
											rotate(a = 180) {
												translate(v = [0, -3, 0]) {
													square(center = true, size = [9, 6]);
												}
											}
											rotate(a = -180) {
												translate(v = [0, -3, 0]) {
													square(center = true, size = [9, 6]);
												}
											}
										}
									}
								}
							}
							rotate(a = -135) {
								translate(v = [0, 47.0000000000, 0]) {
									difference() {
										difference() {
											circle(r = 6);
											rotate(a = 180) {
												translate(v = [0, -6, 0]) {
													square(center = true, size = [18, 12]);
												}
											}
											rotate(a = -180) {
												translate(v = [0, -6, 0]) {
													square(center = true, size = [18, 12]);
												}
											}
										}
										difference() {
											circle(r = 3);
											rotate(a = 180) {
												translate(v = [0, -3, 0]) {
													square(center = true, size = [9, 6]);
												}
											}
											rotate(a = -180) {
												translate(v = [0, -3, 0]) {
													square(center = true, size = [9, 6]);
												}
											}
										}
									}
								}
							}
						}
					}
				}
				translate(v = [44.0000000000, 0, 11.0000000000]) {
					rotate(a = [0, 90, 0]) {
						linear_extrude(height = 10) {
							square(center = true, size = [16.1000000000, 48.1000000000]);
						}
					}
				}
			}
			translate(v = [34.9000000000, 0, 35]) {
				rotate(a = [0, 90, 0]) {
					linear_extrude(height = 16) {
						union() {
							rotate(a = 0) {
								translate(v = [0, 13.5000000000, 0]) {
									circle(r = 8);
								}
							}
							rotate(a = 180) {
								translate(v = [0, 13.5000000000, 0]) {
									circle(r = 8);
								}
							}
						}
					}
				}
			}
		}
		translate(v = [44.0000000000, 0, 11.0000000000]) {
			rotate(a = [0, 90, 0]) {
				translate(v = [-4.0000000000, -20.0000000000]) {
					union() {
						translate(v = [0, 0.0000000000, 0]) {
							union() {
								translate(v = [0.0000000000, 0, 0]) {
									linear_extrude(height = 1.6000000000) {
										circle(d = 4.8000000000);
									}
								}
								translate(v = [8.0000000000, 0, 0]) {
									linear_extrude(height = 1.6000000000) {
										circle(d = 4.8000000000);
									}
								}
							}
						}
						translate(v = [0, 8.0000000000, 0]) {
							union() {
								translate(v = [0.0000000000, 0, 0]) {
									linear_extrude(height = 1.6000000000) {
										circle(d = 4.8000000000);
									}
								}
								translate(v = [8.0000000000, 0, 0]) {
									linear_extrude(height = 1.6000000000) {
										circle(d = 4.8000000000);
									}
								}
							}
						}
						translate(v = [0, 16.0000000000, 0]) {
							union() {
								translate(v = [0.0000000000, 0, 0]) {
									linear_extrude(height = 1.6000000000) {
										circle(d = 4.8000000000);
									}
								}
								translate(v = [8.0000000000, 0, 0]) {
									linear_extrude(height = 1.6000000000) {
										circle(d = 4.8000000000);
									}
								}
							}
						}
						translate(v = [0, 24.0000000000, 0]) {
							union() {
								translate(v = [0.0000000000, 0, 0]) {
									linear_extrude(height = 1.6000000000) {
										circle(d = 4.8000000000);
									}
								}
								translate(v = [8.0000000000, 0, 0]) {
									linear_extrude(height = 1.6000000000) {
										circle(d = 4.8000000000);
									}
								}
							}
						}
						translate(v = [0, 32.0000000000, 0]) {
							union() {
								translate(v = [0.0000000000, 0, 0]) {
									linear_extrude(height = 1.6000000000) {
										circle(d = 4.8000000000);
									}
								}
								translate(v = [8.0000000000, 0, 0]) {
									linear_extrude(height = 1.6000000000) {
										circle(d = 4.8000000000);
									}
								}
							}
						}
						translate(v = [0, 40.0000000000, 0]) {
							union() {
								translate(v = [0.0000000000, 0, 0]) {
									linear_extrude(height = 1.6000000000) {
										circle(d = 4.8000000000);
									}
								}
								translate(v = [8.0000000000, 0, 0]) {
									linear_extrude(height = 1.6000000000) {
										circle(d = 4.8000000000);
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
					rotate(a = -60) {
						translate(v = [0, -50.0000000000, 0]) {
							square(center = true, size = [150.0000000000, 100.0000000000]);
						}
					}
					rotate(a = -120) {
						translate(v = [0, -50.0000000000, 0]) {
							square(center = true, size = [150.0000000000, 100.0000000000]);
						}
					}
				}
				square(center = true, size = [70, 56]);
			}
			union() {
				rotate(a = -45) {
					translate(v = [0, 47.0000000000, 0]) {
						circle(r = 1.5000000000);
					}
				}
				rotate(a = -135) {
					translate(v = [0, 47.0000000000, 0]) {
						circle(r = 1.5000000000);
					}
				}
			}
		}
	}
}
/***********************************************
*********      SolidPython code:      **********
************************************************
 
from __future__ import division

import os, sys

from solid import *
from solid.utils import *
from fixings import M3
from util import *

from sensors import hc_sr04
from raspberrypi import aplus

import lego

FA=0.1
FS=0.5

def bulkhead(radius=50.0):
    def rangesensor():
        return translate([radius - 15 - ABIT , 0, 35])(
            rotate([0, 90, 0])(
                linear_extrude(height=16)(hc_sr04.tranceiver_cut())))

    def lego_position(x):
        return translate([radius - 6, 0, lego.pitch+3])(rotate([0, 90, 0])(x))
    electronics = [max([70, aplus.d[0]]), max(50, aplus.d[1])]
    return ((linear_extrude(height=50.0)(
                (arc(radius, -60, +60) -
                 arc(radius-3, -60, -40) -
                 arc(radius-3, +40, +60) -
                 radial(radius-3, [ -45, -135 ], circle(3) + forward(1.5)(square([6,3], True))) -
                 square(electronics, True)) +
                radial(radius-3, [ -45, -135 ], arc(6, 180, 0) - arc(3, 180, 0))) -
            lego_position(linear_extrude(height=10)(lego.surface(2,6))) -
            rangesensor()) +
            lego_position(lego.studs(2,6)) +
            linear_extrude(height=3)(
                arc(radius, -60, +60) - 
                square(electronics, True) -
                radial(radius - 3, [ -45, -135 ], M3.cut())))

def assembly():
    return bulkhead()
 
if __name__ == '__main__':
    out_dir = sys.argv[1] if len(sys.argv) > 1 else os.curdir
    file_out = os.path.join( out_dir, 'rangebulkhead.scad')
 
    a = assembly()
    print("%(__file__)s: SCAD file written to: \n%(file_out)s"%vars())
    scad_render_to_file( a, file_out, file_header='$fa = %s; $fs = %s;' % (FA, FS), include_orig_code=True)
 
 
************************************************/
