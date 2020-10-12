/**
 * CTF challenges from scratch
 * by Javantea
 * July 22, 2017
 * Updated to be solvable Mar 9, 2019
 * 
 * Heap overflow, exploitable maybe.
 **/

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

void win(int ret);
void (*funcs[2])(int) = {exit, win};

void win(int ret)
{
    printf("flag{heap_overflow_i5_an_art_not_a_sci3nce. Did you?}\n");
    return;
}

int main(int argc, char **argv)
{
	// Unbuffered to fix input issues! yay.
	int r = setvbuf(stdin, 0, _IONBF, 0);
	if(r != 0) {
		printf("ERROR: setvbuf failed\n");
		return 1;
	}
	char *input = 0;
	if(argc < 2) {
		//printf("Usage: easy1 string\n");
		//return 1;
		// 10512 should be enough for anyone.
		input = malloc(11512);
		if(input == 0) return 1;
		int read_len = 0;
		while(read_len < 11512) {
			int flen = read(STDIN_FILENO, input + read_len, 11512 - read_len);
			printf("read %i\n", flen);
			if(flen < 0) break;
			if(flen < 4095) break;
			read_len += flen;
		}
        input[11511] = 0;
	} else {
		input = argv[1];
	}
	if(strlen(input) < (256+sizeof(int *))) {
		printf("1: %s\n", input);
	} else {
		// 10240 should be enough for anyone.
		char *a = malloc(10240);
        a[10239] = 0;
		strcpy(a, input);
		printf("2: %s\n", a);
        printf("%lu %i\n", strlen(input), (int)a[10239]);
        funcs[(int)a[10239]](0);
	}
	return 0;
}
