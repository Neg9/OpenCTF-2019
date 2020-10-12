#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>
#include <unistd.h>
#include <sys/ptrace.h>

#define	ROTATE(ch, perm) (\
    isupper(ch) ? ('A' + (ch - 'A' + perm) % 26) : \
        islower(ch) ? ('a' + (ch - 'a' + perm) % 26) : ch)

char key[] = "SOYOULYKECATS";
char flag[] = "xzyu{h3v0xev4ln}";

char* encrypt(char* msg, char* key)
{
    unsigned int i;
    size_t msglen = strnlen(msg, sizeof(flag));
    char* dec = malloc(msglen * sizeof(char));
    for(i = 0; i < msglen; i++)
    {
        int rot = toupper(key[i % strlen(key)]) - 'A';
        dec[i] = ROTATE(msg[i], rot);
    }
    return dec;
}

void bail(char* msg)
{
    printf(msg);
    kill(getpid(), SIGKILL);
    exit(0);
}

__attribute__  ((constructor)) void check()
{
    if (getenv("LD_PRELOAD"))
        bail("hope you didn't think i was that easy..\n");
    if (ptrace(PTRACE_TRACEME, 0, 0, 0) < 0)
        bail("you..\nyou people..\npoking and prodding...\n");
}

int main()
{
    char *answer = NULL;
    size_t answerlen = 0;

    printf("Do you know?\n");
    printf("Tell me: ");
    getline(&answer, &answerlen, stdin);
    strtok(answer, "\n");
    answer = encrypt(answer, key);
    if (strcmp(answer, flag) == 0)
        printf("You got it!\n");
    else
        printf("You don't know, huh?\n");
}
