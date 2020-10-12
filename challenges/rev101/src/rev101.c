#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// stolen from bsdgames: caesar.c
#define	ROTATE(ch) (\
    isupper(ch) ? ('A' + (ch - 'A' + 13) % 26) : \
        islower(ch) ? ('a' + (ch - 'a' + 13) % 26) : ch)

char key[] = "synt{vy0i3p4gm}";

void usage(progname)
char* progname;
{
    printf("Usage: %s KEY", progname);
    exit(2);
}


int main(argc, argv)
int argc;
char *argv[];
{
    unsigned int i;

    if (argc != 2)
        usage(argv[0]);

    for (i = 0; i < strlen(key); i++)
        if (key[i] != ROTATE(argv[1][i]))
            goto fail;

    printf("Correct Key Found");
    return 0;

    fail:
        printf("WRONG");
        return 1;
}
