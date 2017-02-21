include $(wildcard *.deps)

%.stl: %.scad
	openscad -m make -o $@ -d $@.deps $<

stlink.zip: nucleo_f303re_swd.stl nucleo_stlink_base.stl nucleo_stlink_lid.stl nucleo_stlink_swd.stl
	zip $@ $+

all: stlink.zip
