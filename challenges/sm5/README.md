# Game Copy Protection ROM
*by Javantea*  
*July 31, 2019*

Score:
100

Description:

To reverse engineer a 33-year-old video game chip John McMaster got a microscope off craigslist, motor controllers out of university dumpster, and a laptop from a surplus shop. He used an arm chip and some python to control the motors and take photos. Then he put on a hazmat suit and delayered the chip with ammonium fluoride, a temperature controlled heat gun, and a vortexer. Then he dash etched with HNO3 and HF to get the bits to show up on the microscope. Then MarshallH wrote a bunch of C# to pull the bits off the images. It turns out that it's not all that difficult to understand. It's just security through obscurity. Pull the authentication stream. Might as well write your own implementation while you're at it. This challenge has a non-standard flag format, the first 5 letters are f149{.

Category: reversing

Build:
```
make
or
python3 sm5asm.py -o sm5_flag.o sm5_flag.S

```

Notes:

* If they can't find the talk, just give them the damn youtube link but make it difficult.
* If they don't have time to watch the talk, here's a recap you can give them:
  1. Shave a yak
  2. The way Nintendo was able to avoid competing publishers (*cough*antitrust*cough*) on their platform was to add a chip that produced a pseudorandom stream that had a complementary chip.
  3. To fully reproduce that chip on commodity hardware like an ATMega or ARM chip, you need:
    * the algorithm which is on the ROM
    * the complete architecture of the chip
    * to be able to also implement the algorithm in C/ASM/python/whatever
  4. This challenge is much easier because the chip isn't going to produce a pseudorandom stream.
