# Solution to sm5 (aka Game Copy Protection ROM)
*by Javantea*  
*May 11, 2019*

The hint will hopefully give you the talk. The talk gives you the name of the people that you need to find sm5emu.
https://github.com/mikeryan/sm5emu.git

We use a modified version of sm5emu that prints A on op_OUT and does a bunch of other things like exit when you ctrl-d.

```
git diff > sm5emu-javantea.patch

~/src/sm5emu/sm5emu dump.bin >solve4a.txt
sm5emu: File too short
sm5emu: File too short
r
q
```

You *must* modify solve4a.txt so that all OUT are on the beginning of the line.

```
cut -d ' ' -f 2 < solve4a.txt |tr -d '\n'; echo
:663134397b526576657273696e6720746865204e696e74656e646f20363420434943202d205245636f6e20323031357dHalted:

python3
import binascii
binascii.unhexlify('663134397b526576657273696e6720746865204e696e74656e646f20363420434943202d205245636f6e20323031357d')
b'f149{Reversing the Nintendo 64 CIC - REcon 2015}'
```

So the question you might be wondering is why would they be interested in the OUT command? If you look at the original hack, the team spent countless hours trying to figure out what the heck was going on in commands. In order to solve this, you need to understand what might be happening with our commands. It won't just print the solution when you run it with the off-the-shelf emulator because 

emulators    have      bugs.

