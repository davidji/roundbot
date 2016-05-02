
A rotary encoder generates two signals. Going forward, one signal will
be 90 degrees forward of the other, and going in reverse, the oposite.

I think that means I need a sample rate 4x the rate I need to capture
the rate.

The encoders have 3 arms or 5 arms, I think this means 3x or 5x the
frequency of the motor.

So in the worst case with 5 arms, no load speed of 30K RPM:

30K RPM = 520Hz
520 * 5 * 4 * 2 = 20KHz

Lets say 25KHz. 2 channels, and two motors, so our ADC needs to run at 100KHz.
8 bits should be plenty of resolution.

I don't think I need to do a fourier transform: I can presumably just look for
zero crossing points. In fact I pretty much need to count events.

This suggests I don't need watchdog hardware: I just use one ADC for this purpose,
and then process a modest data stream in slightly less than real time.

