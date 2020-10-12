/*
Antisat
by Javantea
May 24, 2016

All right granted to Neg9 members.
gcc -o antisat antisat.c -Wall -ggdb -O2
*/
#include <stdio.h>
#include <stdlib.h>

int f(int x, int y, int z, int nine)
{


	int v = x + y;
	int w = x ^ z;
	
	int t = x & 0xff11ff;
	int u = y + 0xff11ff;
	int a = z * nine;
	int b = (z * t) % 0x33333;
	return (v + w + t) ^ ((u & a) * b);

}

int main(int argc, char **argv)
{
	if (argc < 2) {
		printf("Usage: ./antisat num\n");
		return 1;
	}
	int r = atoi(argv[1]);
	int i;
	for(i = 0; i < 1000000; i++)
	{
		r = f(i, r, 393, 99993);
		printf("%i\n", r);
	}
	if(r == 178104981) {
		printf("Good job! flag{%s}\n", argv[1]);
		return 0;
	}
	printf("See ya later.\n");
	return 1;
}
