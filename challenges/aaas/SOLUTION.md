# AAAS Solution

*by Javantea*  
May 18, 2019 and June 9, 2019

This challenge is a simple straightforward RNG cracking exercise. It's slow on the user side, fast on the challenge side.

This challenge requires you to realize that the program uses your e-mail address unsalted as a seed for a rng. Then you have to realize that the number given is the first output of the rng. Then you have to crack an input that will give an output of 987654321. It's parallel, so you can run as many processes as you have cores. It doesn't take long because it's random.seed(s) random.randint(0, 0xffffffff) which you can learn from the values it returns to you and guessing. What you might not guess is that it's not the first output that it's checking to give you the flag, it's the second value. So once you're done cracking, you have to crack a second time.

```
python3 solve.py 2 &
python3 solve.py 3 &
python3 solve.py 4 &
python3 solve.py 5 &
python3 solve.py ein &
python3 solve.py sechs &
python3 solve.py elf &
python3 solve.py zwolf &
python3 solve.py gally &
wait

```
