
# Solution

There are three discrete but sequential challenges on the ATTiny85 hw hacking challenge.

The following PDF shows the PIN diagram, note that pins 0-4 are labeled in blue.
https://cdn.sparkfun.com/assets/2/8/b/a/a/Tiny_QuickRef_v2_2.pdf


## Level 1

The goal of level one is to discover that pins 3 & 4 are RX and TX for a UART serial
connection respectively. This can be discovered rather quickly with a logic analyzer
or by trial and error with an FTDI friend or other UART cable. The trick is to calculate
the appropriate BAUD rate by analyzing the signal frequency. Also, there are only so many
standard BAUD rates, so brute force would be simple. Once the player has the UART connection 
to their laptop (e.g. screen), they will discover the chip is broadcasting "OpenCTF 2019"
every few seconds. The chip is waiting for user input on the serial connection, merely 
pressing enter will suffice, and it will print the first flag.

```
$ screen -S foo /dev/ttyUSB0 19200

OpenCTF 2019
OpenCTF 2019
OpenCTF 2019
OpenCTF 2019
OpenCTF 2019
Congratz, the level 1 flag is: tHe_bEau7y_0f_7h3_BAUD
Welcome to level 2!
```

