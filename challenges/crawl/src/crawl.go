package main

import "os"
import "fmt"
import "math/rand"
import "crypto/md5"


type Dungeon struct {
    level int
    player Player
    dungeon []Level
}

func ascend(d *Dungeon) {
    d.level -= 1
}

func descend(d *Dungeon) {
    d.level += 1
}

func fight(d *Dungeon) {
    monsters := d.dungeon[d.level].monsters
    player := d.player
    fmt.Printf("You engage %d enemies\n", len(monsters))
    for {
        fmt.Printf("Your HP: %d\n", player.hp)
        fmt.Printf("Choose your target:\n")
        fmt.Printf("\t#\tName\tHP\n")
        for i, monster := range monsters {
            if monster.hp != 0 {
                fmt.Printf("\t%d\t%s\t%d\n", i, monster.name, monster.hp)
            }
        }
        target := 0
        _, err := fmt.Scanf("%d", &target)
        if err != nil {
            panic(err)
        }
        monster := &monsters[target]

        // check if attack hits
        hit := rand.Intn(20)
        if hit > 8 {
            damage := uint32(rand.Int31n(12) + 4)
            fmt.Printf("You strike, and hit, dealing %d damage.\n", damage)
            if damage > monster.hp {
                monster.hp = 0
            } else {
                monster.hp -= damage
            }
            fmt.Printf("They have %d hp left.\n", monster.hp)
            if (monster.hp <= 0) {
                fmt.Printf("You slay a %s, nice work.\n", monster.name)
            }
        } else {
            fmt.Printf("You swing and miss.\n")
        }

        // check if all monsters are killed
        totalhp := uint32(0)
        for _, monster := range monsters {
            totalhp += monster.hp
        }
        if (totalhp == 0) {
            break
        }

        // monster's turn
        for _, monster := range monsters {
            hit := rand.Intn(20)
            if hit > 18 {
                damage := uint32(rand.Int31n(12))
                fmt.Printf("The %s strikes you, dealing %d damage.\n", monster.name, damage)
                if damage > player.hp {
                    player.hp = 0
                } else {
                    player.hp -= damage
                }
                if (player.hp <= 0) {
                    fmt.Printf("You have died.\n")
                    os.Exit(1)
                }
            } else {
                fmt.Printf("The %s tries to attack, but misses you\n", monster.name)
            }

        }
    }
}

func open(d *Dungeon) {
    var pass string
    fmt.Printf("What be the code? ")
    _, err := fmt.Scanf("%s", &pass)
    if err != nil {
        fmt.Printf("Did you get the instructions?\n")
    }
    if "51be3a34d5fa172d4f86980196722124" == fmt.Sprintf("%x", md5.Sum([]byte(pass))) {
        fmt.Printf("As you open the chest, you find a flag.\nFuck yea\n")
        os.Exit(0)
    } else {
        fmt.Printf("Uhh, nope.\nYou hear a clicking sound.\nThe chest explodes.\nYou have died.\n")
        os.Exit(1)
    }
}

type Level struct {
    dungeon *Dungeon
    desc string
    choices []Choice
    monsters []Monster
}

func (level Level) printChoices() {
    for i, choice := range level.choices {
        fmt.Printf("%d: %s\n", i, choice.desc)
    }
    fmt.Printf("What would you like to do? ")
}

func (level Level) getChoice() {
    var o int
    _, err := fmt.Scanf("%d", &o)
    if err != nil {
        panic(err)
    }
    level.choices[o].action(level.dungeon)
}

type Choice struct {
    desc string
    action func(*Dungeon)
}

type Player struct {
    hp uint32
    inventory Inventory
}

type Inventory struct {
    torch bool
}

type Monster struct {
    hp uint32
    name string
}

var dungeonlevels = []Level {
    Level {
        desc: "As you enter the fabled dungeon, you see skeletons lining the floor.\nA great battle happened here once. Among the dead, are orcs, and dwarves.",
        choices: []Choice {
            {"Flee the dungeon", func (d *Dungeon) { os.Exit(0) }},
            {"Continue deeper", descend,},
        },
    },
    Level {
        desc: "As you descend the stairs, the natural light fades. You can't see anything.",
        choices: []Choice {
            {"Go back up", ascend},
            {"Continue deeper", descend},
            {"Light a torch", func (d *Dungeon) { d.player.inventory.torch = true }},
        },
    },
    Level {
        desc: "You find yourself surrounded by 3 goblins. Fortunately you came prepared.",
        choices: []Choice {
            {"Go back up", ascend},
            {"Continue deeper", descend},
            {"Fight", fight},
        },
        monsters: []Monster {
            {12, "Goblin"},
            {12, "Goblin"},
            {12, "Goblin"},
        },
    },
    Level {
        desc: "The room is entirely empty except for a jewel encrusted chest. There are 10 jewels inlaid the chest.",
        choices: []Choice {
            {"Go back up", ascend},
            {"Continue deeper", descend},
            {"Open Chest", open},
        },
    },
}

func main() {
    var d Dungeon
    d.dungeon = dungeonlevels
    for ; d.level < len(d.dungeon); {
        level := d.dungeon[d.level]
        d.player.hp = 20
        level.dungeon = &d

        fmt.Printf("%s\n\n", level.desc)

        level.printChoices()
        level.getChoice()
    }
}
