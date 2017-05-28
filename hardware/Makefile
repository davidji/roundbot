include $(wildcard *.deps)

%.stl: %.scad
	openscad -m make -o $@ -d $@.deps $<

stlink.zip: nucleo_f303re_swd.stl nucleo_stlink_base.stl nucleo_stlink_lid.stl nucleo_stlink_swd.stl
	zip $@ $+

cr123a-cover-1.scad cr123a-holder-1.scad cr123a-cover-2.scad cr123a-holder-2.scad cr123a-cover-3.scad cr123a-holder-3.scad cr123a-cover-4.scad cr123a-holder-4.scad: cr123a-holder-.py
	python $+

cr123a.zip: cr123a-cover-1.stl cr123a-holder-1.stl cr123a-cover-2.stl cr123a-holder-2.stl cr123a-cover-3.stl cr123a-holder-3.stl cr123a-cover-4.stl cr123a-holder-4.stl
	zip $@ $+

all: stlink.zip cr123a.zip

head.scad: head.py
	python head.py

clean:
	rm -f *.stl *.stl.deps *.scad *.pyc *.zip
