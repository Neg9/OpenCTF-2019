/*
FTL-alike game using C and printf
by Javantea
Nov 19, 2017
*/
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <limits.h>
#include <string.h>
#include <time.h>
#include <error.h>

struct room;

struct room {
    char *name;
    int purpose;
    struct room *neighbors;
};

struct ship {
    char *name;
    struct room *rooms;
};

struct player {
    char *name;
    struct room *room;
};

struct npc {
    char *name;
    struct room *room;
};

// purposes
#define BRIDGE 1
#define ENGINES 2
#define WEAPONS 3
#define CAFE 4
#define QUARTERS 5
#define MEDICAL 6
#define SCIENCE 7
#define RECREATION 8
#define AGRICULTURE 9
#define OPERATIONS 10
char *names[] = {"", "Bridge", "Engines", "Weapons", "Cafe", "Quarters", "Medical", "Science", "Recreation", "Agriculture", "Operations"};

int get_name(const char *name)
{
    const char *p = name;
    //printf("In Name: %s\n", p);
    while(p[0] == ' ') {
        p++;
    }
    //printf("Name: %s\n", p);
    int i;
    for(i = 0; i < sizeof(names)/sizeof(char *); i++)
    {
        if(0 == (strcmp(names[i], p)))
        {
            return i;
        }
    }
    return 0;
}

int main(int argc, char **argv)
{
	struct ship e;
    struct player player;
    struct npc *npcs = malloc(sizeof(struct npc) * 270);
    if(npcs == 0)
    {
        perror("malloc");
        return 1;
    }
    int rooms = 10;
    int i;
    char command[1024];
    command[0] = '\0';
    e.name = "";
    if(argc > 1)
    {
        e.name = argv[1];
    }
    e.rooms = malloc(sizeof(struct room) * rooms);
    if(e.rooms == 0)
    {
        perror("malloc");
        return 1;
    }
    for(i = 0; i < rooms; i++)
    {
        e.rooms[i].purpose = i + 1;
        e.rooms[i].name = names[i + 1];
        e.rooms[i].neighbors = 0;
    }
    while(1)
    {
        fgets(command, 150, stdin);
        int line_len;
        for(line_len = 0; line_len < 150; line_len++)
        {
            if(command[line_len] == '\n') {
                command[line_len] = 0;
                break;
            }
        }
        //printf("%s\n", command);
        if(0 == strcmp(command, "quit")) break;
        if(0 == strcmp(command, "q")) break;
        if(0 == strcmp(command, "exit")) break;
        if(0 == strncmp(command, "go", 2)) {
            // goto a certain room
            int room = get_name(command + 2);
            if(room > 0) {
                player.room = &(e.rooms[room - 1]);
                printf("In %s\n", player.room->name);
            }
        }
    }
    free(e.rooms);
    
    return 0;
}
