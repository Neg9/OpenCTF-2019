/*
FTL-alike game using C and printf
by Javantea
Nov 18, 2017

f1a9{Debbie for Captain siatyVUdn6A}

Hide the constants in the solution. Enough constants, it's impossible to brute.

def mash(b, i):
    output = b
    output *= 3
    output ^= 0x71
    output -= i
    output += i*i*i*33
    return output & 0x7f
#end def mash(b, i)

flag_int = [ord(f) for f in 'f1a9{Debbie for Captain siatyVUdn6A}']

[flag_int[i] in [mash(v, i) for v in range(256)] for i in range(len(flag_int))]

[[mash(v, i) for v in range(256)].index(flag_int[i]) for i in range(len(flag_int))]
[93, 32, 14, 16, 26, 31, 118, 65, 9, 88, 82, 35, 65, 18, 19, 27, 54, 112, 25, 15, 108, 64, 95, 11, 126, 56, 54, 63, 12, 85, 46, 103, 85, 13, 14, 60]

*/

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <limits.h>
#include <string.h>
#include <time.h>

#ifndef DEBUG
#define DEBUG 0
#endif //

struct node;

struct node {
    int x, y;
    struct node **conns;
};

void f71_abort(const char *s)
{
    perror(s);
    exit(1);
}

int pow_of_two(int n)
{
    int i;
    for(i = 1; i < n; i <<= 1);
    return i;
}

int randint_mask(int start, int end, int mask)
{
    int x = start + (random() & mask);
    if(x >= end) {
        x -= (end - start);
    }
    return x;
}

// Very slow randint using modulus.
int randint(int start, int end)
{
    return start + (random() % (end - start));
}

struct node *graph(int nodes, int conns)
{
    if(nodes > INT_MAX / sizeof(struct node)) {
        fprintf(stderr, "Error: Graph is too big.\n");
        return 0;
    }
    struct node *output = malloc(sizeof(struct node) * nodes);
    if(output == 0) f71_abort("malloc");
    memset(output, 0, sizeof(struct node) * nodes);
    int pos_x = 0, pos_y = 0;
    int i, j, x;
    int conns_curr = 0;
    int mask = pow_of_two(nodes) - 1;
    if(mask < nodes) {
        // Nodes is a power of two. Increase.
        mask = ((mask + 1) << 1) - 1;
    }
    for(i = 0; i < nodes; i++)
    {
        output[i].x = pos_x;
        output[i].y = pos_y;
        pos_x++;
        if(conns_curr < conns) {
            // Evenly distribute conns because it's silly.
            int to_conn = (conns - conns_curr) / (nodes - i);
            output[i].conns = malloc(sizeof(struct node *) * (to_conn + 1));
            if(output[i].conns == 0) f71_abort("malloc");
            for(j = 0; j < to_conn; j++) {
                // FIXME: often connect things to themselves I think.
                // Very weak and fast rng
                x = randint_mask(0, nodes, mask);
                output[i].conns[j] = output + x;
                conns_curr++;
            }
            output[i].conns[j] = 0;
        }
    }
    return output;
}

int graph_destroy(struct node *g, int nodes)
{
    int i;
    for(i = 0; i < nodes; i++)
    {
        if(g[i].conns) {
            free(g[i].conns);
            g[i].conns = 0;
        }
    }
    free(g);
    return 0;
}

int graph_draw(struct node *g, int nodes)
{
    int i, j;
    for(i = 0; i < nodes; i++)
    {
        printf("%i", i);
        if(g[i].conns) {
            for(j = 0; g[i].conns[j]; j++) {
                printf(" -- %li", g[i].conns[j]-g);
            }
        }
        printf("\n");
    }
    return 0;
}

/**
 * There are many ways to guarantee a path.
 * The one I'm going to try is to modify any loop to include the exit.
 **/
int guarantee_path(struct node *g, int nodes, int start, int dest)
{
    int i, j, next;
    int current = start;
    for(i = 0; i < 100; i++)
    {
        if(g[current].conns) {
            next = g[current].conns[0]-g;
            for(j = 0; g[current].conns[j]; j++) {
                next = g[current].conns[j]-g;
                if(dest == next) return 0;
            }
            current = next;
        }
    }
    if(g[current].conns == 0)
    {
        g[current].conns = malloc(sizeof(struct node *) * 2);
        if(g[current].conns == 0) f71_abort("malloc");
        g[current].conns[0] = &(g[dest]);
        g[current].conns[1] = 0;
    }
    else
    {
        // FIXME: This does not guarantee by a long shot.
        g[current].conns[0] = &(g[dest]);
        return 1;
    }
    return 0;
}

int get_conns(struct node **c)
{
    int j;
    for(j = 0; c[j]; j++);
    return j;
}

/**
 * There are many ways to guarantee a path.
 * The one I'm going to try is to modify any loop to include the exit.
 **/
int guarantee_path2(struct node *g, int nodes, int start, int dest, int length)
{
    int i, x, y, conns;
    int mask = pow_of_two(nodes) - 1;
    if(mask < nodes) {
        // Nodes is a power of two. Increase.
        mask = ((mask + 1) << 1) - 1;
    }
    int current = start;
    for(i = 0; i < length; i++)
    {
        if(g[current].conns == 0) {
            g[current].conns = malloc(sizeof(struct node *) * 2);
            if(g[current].conns == 0) f71_abort("malloc");
            g[current].conns[0] = &(g[current]);
            g[current].conns[1] = 0;
        }
        conns = get_conns(g[current].conns);
        x = randint(0, conns);
        if(i < (length - 1))
        {
            y = randint_mask(0, nodes, mask);
            if(y == dest)
            {
                y++;
            }
            if(y >= nodes)
            {
                y = 0;
            }
        }
        else
        {
            y = dest;
        }
        // Useful for test, short solves
        //fprintf(stderr, "connecting %i %i\n", current, y);
        g[current].conns[x] = &(g[y]);
        current = y;
    }
    return 0;
}

// From oryx_part4a1a1a1.c
int a_in_b(int a, int *b, int length)
{
        int i;
        for(i = 0; i < length; ++i)
        {
                if(a == b[i]) {
                        return 1;
                }
        }
        return 0;
}

// Plenty long.
#define HISTORY_LEN 400

int main(int argc, char **argv)
{
    // FIXME: random for the game, not for testing.
    srand(time(0) ^ (getpid() << 3) ^ 0x0f710f71 ^ (long)graph);
    //srand(0xf71);
    printf("F71\n");
    int nodes = 10;
    int conns = 11;
    int debug = DEBUG;
    int zones = 7, zone;
    int beers = 0;
    int blue_event = 0;
    int an_alien = 0;
    int i, j, length;
    int history_i;
    int history[HISTORY_LEN];
    //char flag[] = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ012345679";
    //char flag[] = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA";

    char flag[] = {93, 63, 14, 10, 26, 31, 118, 65, 9, 88, 82, 35, 65, 18, 19, 27, 54, 112, 25, 15, 108, 64, 95, 11, 126, 56, 54, 63, 12, 85, 46, 103, 85, 13, 14, 60, 0};
    int flag_len = strlen(flag);
    if(argc > 1)
    {
        nodes = atoi(argv[1]);
    }
    if(argc > 2)
    {
        conns = atoi(argv[2]);
    }
    for(zone = 0; zone < zones; zone++)
    {
        printf("Zone %i\n", zone);
        history_i = 0;
        struct node *g = graph(nodes, conns);
        if(g == 0)
        {
            return 1;
        }
        length = randint_mask(1, 10, 0xf);
        int r = guarantee_path2(g, nodes, 0, nodes - 1, length);
        //int r = guarantee_path(g, nodes, 0, nodes - 1);
        // FIXME: guarantee_path2 only ever returns 0! They never get the blue alien event or the hobbies event!
        //if(r == 1)
        if(randint(0, 13) == 4)
        {
            if(blue_event == 0)
            {
                printf("You meet a beautiful blue alien.\nPick her up?\n");
                char response = 0;
                for(i = 0; i < 4; ++i)
                {
                    int rr = scanf("%c", &response);
                    printf("response %i %c %i\n", response, response, rr);
                    if(response == 'y' || response == 'n' || response == 'Y' || response == 'N') break;
                }
                if(response == 'Y' || response == 'y')
                {
                    blue_event++;
                }
            } 
            else
            {
                printf("You meet an alien. You two share similar hobbies.\n");
                an_alien++;
            }
        }
        if(debug == 2) {
            
            printf("g = {\n");
            for(i = 0; i < nodes; i++)
            {
                printf("  %c {%i, %i, {", 'a'+i, g[i].x, g[i].y);
                if(g[i].conns) {
                    for(j = 0; g[i].conns[j]; j++) {
                        char r = g[i].conns[j] - g;
                        printf("%c, ", 'a'+r);
                    }
                }
                printf("}}\n");
            }
            printf("}\n");
        } else {
            graph_draw(g, nodes);
        }
        int current_node = 0;
        while(current_node != (nodes - 1))
        {
            printf("You are at %i. You want to get to %i.\n", current_node, nodes - 1);
            printf("Next node: ");
            fflush(stdout);
            int next = 0;
            int x = scanf("%i", &next);
            printf("x %i\n", x);
            if(x == -1) {
                return 0;
            }
            else if(x == 0) {
                // No reason, I'm just a big fan of reading.
                char buf[1024];
                int z = fread(buf, 1024, 1, stdin);
                printf("z %i\n", z);
                continue;
            }
            if(history_i < HISTORY_LEN)
            {
                history[history_i++] = next;
            }
            if((next < 0) || next > nodes)
            {
                printf("Invalid node\n");
                continue;
            }
            int found = 0;
            if(g[current_node].conns) {
                for(j = 0; g[current_node].conns[j]; j++) {
                    int r = g[current_node].conns[j] - g;
                    if(r == next)
                    {
                        found = 1;
                        current_node = next;
                        break;
                    }
                }
            }
            if((0 == found) && (next >= 0) && (next < nodes) && g[next].conns) {
                for(j = 0; g[next].conns[j]; j++) {
                    int r = g[next].conns[j] - g;
                    if(r == current_node)
                    {
                        found = 1;
                        current_node = next;
                        break;
                    }
                }
            }
            if(found && (a_in_b(next, history, history_i-1) == 0))
            {
                printf("You met some friendly aliens. They shared a beer with you.\n");
                beers++;
            }
        }
        graph_destroy(g, nodes);
        g = 0;
    }
#if DEBUG == 1
    printf("debug beers %i blue event %i an alien %i\n", beers, blue_event, an_alien);
#endif // DEBUG
    if(beers >= 99)
    {
        if(beers < 0x71) {
		puts("You find an alien rune. You're not nearly drunk enough to interpret it.\n");
        } else if (beers > 0x71) {
		puts("You are so drunk you could probably the entire universe right now.\n");
        }
        //puts(flag);
        for(i = 0; i < flag_len; i++) {
            flag[i] *= 3;
            flag[i] ^= beers; // 0x71 is the solution.
            flag[i] -= i;
            flag[i] += i*i*i*33;
            flag[i] &= 0x7f;
            //printf("%i ", flag[i]);
        }
        //printf("\n");
        puts(flag);
        puts("\n");
    }
    else
    {
       puts("A sober man once said crypto was for the innocent. What did the drunk man say?\n");
       puts(flag);
       puts("\n");
    }
    if((blue_event == 1) && (an_alien == 1))
    {
        printf("You and the blue alien head toward the first star on the left and on until morning.\n");
    }
    return 0;
}
