
# Solution

There are three discrete but sequential challenges on the ATTiny85 hw hacking challenge.

The following PDF shows the PIN diagram, note that pins 0-4 are labeled in blue.
https://cdn.sparkfun.com/assets/2/8/b/a/a/Tiny_QuickRef_v2_2.pdf


## Level 3

Once the level 2 flag is entered correctly, the chip welcomes the player level 3 and goes
silent and does not accept any additional input on the serial connection. The player will
need to use a logic analyzer, voltmeter, or LED to discover that PIN 2 is now actively
broadcasting a signal (it was not active during level 1). The signal timing has been carefully
chosen to be solvable without a logic analyzer and common logic analyzer software will not
correctly auto-decode the signal. It is Morse code. However, if they hook up an LED they can 
use an android app to decode the Morse, it's slow enough that it could be tediously transcribed 
by hand (possible but really hard, take a video and slow it down would help). 


```
-. ...-- ...- ...-- .-. ..--.- ... . -. -.. ..--.- .- ..--.- -... ----- -.-- ..--.- --... --- ..--.- -.. ----- ..--.- .- ..--.- .-- ----- -- .- -. ..... ..--.- .--- --- -...
N3V3R_SEND_A_B0Y_7O_D0_A_W0MAN5_JOB
```


