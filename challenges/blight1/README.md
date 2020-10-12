#Blight 1
*by Javantea*  
*Feb 16, 2019*

Score:
100

Description:
One of many good RF challenges. We give them an IQ file, they decode, return for points.
GFSK is a common mode in radio communication featured in Bluetooth among others.
Can you decode values that have been transmitted?
You should be able to send this through GFSK demod and get the flag.
blight1.bin is untampered.
blight1a.bin is tampered using blight1a.py

Category: misc

Build:
* On Gentoo: emerge -av gnuradio
* On other systems: compile blight1.grc into blight1.py
* Run blight1.py which creates blight1.bin.
* Run blight1a.py which creates blight1a.bin which is the challenge binary.

Notes:
The question running through my mind is.. Can I recover FM? Can I recover AM? Can I recover SSB? Can I recover morse? Yes.
It was actually easy enough that I think people will enjoy it.

Let's create one challenge for each. Perhaps we could combine into one gigantic flag?

The flag is guessable, but only if you know what it looks like or sounds like. I'll change that.


