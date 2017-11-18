
Motor controller with low voltage cutoff, reverse voltage protection
and push on/push off switch.

Calculation for divider resistors

VS = switch voltage i.e. the switch off voltage = 6.6V minimum
VD1 = voltage drop across the diode D1

R4/(R4 + R7) <= 1.24/(VS - VD1)

I'm going to pick R4 = 15K

That means the current at the switching voltage will be 1.24/15K = 0.08mA so VD1 ~ 0.5V

(R4 + R7)/R4 >= (VS - VD1)/1.24
R7 >= R4*(VS - VD1)/1.24 - R4
   >= 15K*6.1/1.24 - 15K
   >= 58K
   = 62K (E24)

VS = 1.24*(R4+R7)/R4 + VD1
   = 6.865V

That's OK. Also, If I choose R2 = 68K

VS2 = The minimum switch on voltage
    = 1.24*(R4+R2)/R4
    = 6.861V

which matches very closely.

The cathode current for IC1 (TS432A) is determined by R1. It needs to be > 80uA. The maximum value for
R1 at 6.6V is then 82K. I seem to be getting away with less - and that's because the typical
minimum is actually 20uA, but there's no point relying on that.

The application circuit for the TS43A most like mine is the series pass regulator - because
there's in effect no load. It has a capacitor between the cathode and reference, which
wasn't in my first version of the design.


