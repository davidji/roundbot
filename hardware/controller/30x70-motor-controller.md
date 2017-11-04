
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

That's not ideal, but OK.

Also, If I choose R2 = 68K

VS2 = The minimum switch on voltage
    = 1.24*(R4+R2)/R4
    = 6.861V

which matches very closely.


