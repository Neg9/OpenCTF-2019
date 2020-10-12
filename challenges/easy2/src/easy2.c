/**
 * CTF challenges from scratch
 * by Javantea
 * July 22, 2017
 * Modified to use easy1's dual input Mar 15, 2019.
 * 
 * Stack overflow, likely exploitable.
 **/

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

int main(int argc, char **argv)
{
	// Unbuffered to fix input issues! yay.
	int r = setvbuf(stdin, 0, _IONBF, 0);
	if(r != 0) {
		printf("ERROR: setvbuf failed\n");
		return 1;
	}
	printf("system: %p\n", system);
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
		printf("%s\n", input);
	} else {
		// 10240 should be enough for anyone.
		char a[10240];
		memcpy(a, input, 10386);
		printf("%s\n", a);
	}
	return 0;
}
