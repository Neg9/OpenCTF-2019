# Blight1 Solution
*by Javantea*  
June 2, 2019

## Setup

```
apt install gnuradio
```

## Directions

blight1_soln.py decodes the GFSK and outputs the solution to /home/jvoss/sno/rf2/blight1a_soln.out. It should look like the value in blight1a_soln.out which is the flag.

If you are wondering why you would pick GFSK to demodulate this, the number of modulations currently in use in RF are: AM, FM, PM, QAM, SM, SSB, ASK, APSK, CPM, FSK, MFSK, MSK, OOK, PPM, PSK, SC-FDE, TCM, WDM, and OFDM. GFSK is a fix for FSK which is so popular that it is essentially top 10. When you look at this in an RF scope, you should recognize it as GFSK.
