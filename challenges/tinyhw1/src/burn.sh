#!/bin/bash

AVRDUDE="/opt/arduino-1.8.9/hardware/tools/avr/bin/avrdude"
AVRCONF="/opt/arduino-1.8.9/hardware/tools/avr/etc/avrdude.conf"
AVRCMD="$AVRDUDE -C$AVRCONF -v -v -pattiny85 -cusbtiny"
# alias my-avrdude="$AVRCMD"

INOHEX="tinyhw123.ino.hex"

if [ "$1" == "read" ]; then

   # flash
   $AVRCMD -U flash:r:flash.bin:r

   # fuses
   $AVRCMD -U efuse:r:efuse.bin:r
   $AVRCMD -U hfuse:r:hfuse.bin:r
   $AVRCMD -U lfuse:r:lfuse.bin:r
   
   # eeprom
   $AVRCMD -U eeprom:r:eeprom.bin:r

   # lock
   $AVRCMD -U lock:r:lock.bin:r 

elif [ "$1" == "write" ]; then

   # erase chip, set fuses
   $AVRCMD -e -U efuse:w:0xff:m -U hfuse:w:0xdf:m -U lfuse:w:0xe2:m 

   # write flash
   $AVRCMD -U flash:w:$INOHEX:i 

   # lock
   $AVRCMD -U lock:w:0xfc:m

else 
   echo "$0 [read|write]"

fi

