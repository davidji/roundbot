
A rotary encoder generates two signals. Going forward, one signal will
be 90 degrees forward of the other, and going in reverse, the opposite.

If the signal was digital, I could be interrupted on the rising edge
of one signal, capture the value of the other signal and use that as
the direction.

The capture needs to happen within 1/8th of the period of the encoder
signal to be reliable.

The motor could run up to 30K RPM, The encoders have 3 arms or 5 arms, 
I think this means the signal is 3x or 5x the frequency of the motor.
This is (30K/60)*5 = 2.5KHz, so the period is 400us.

mbed only offers one way of sampling - which is ask for a sample and
wait until it's done, but the STM32F303K8 can complete a sample in 0.2us!
Even if mbed is insanely inefficient, I should be able to do this without
any additional hardware: I can use the ADC and signal processing.

400us/8 = 50us. I need to sample every 50us in order to be within 1/8th of the
zero crossing. When that happens, I do another sample.

It's worth just checking how many instructions get executed in 50us -
at 72MHz it's about 350. That's not a huge number.

Notice the hardware could just sample both channels on a schedule,
and interrupt the application on completion. If I used Chibios I
could easily do this.

