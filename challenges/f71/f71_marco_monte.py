#!/usr/bin/env python3
"""
This the rhythm of the night the night oh yeah
by Javantea
May 21, 2019

# This doesn't work, so I'm gonna user script.
while true; do i="$(($i+1))"; python3 f71_marco_monte.py >f71_marco_monte_debug.txt; tail -n 3 f71_marco_monte_debug.txt; tar cJf itworks/f71r"$i".tar.xz f71_marco_monte_debug.txt lp?.json; rm lp?.json f71_marco_monte_debug.txt; done

script solutions_s.txt
while true; do i="$(($i+1))"; python3 f71_marco_monte.py; tar cJf itworks/f71s"$i".tar.xz lp?.json; rm lp?.json; done
"""
import pexpect
import sww.mapmake1

Map = sww.mapmake1.Map
Point = sww.mapmake1.Point

nodes = 22
conns = 30
child = pexpect.spawn(' '.join(['./f71', str(nodes), str(conns)]))

lp_filename_i = 0

def get_io():
    """
    Holy shit, this works.
    """
    data = b''
    while True:
        if not child.isalive():
            print("e's dead Jim")
            break
        x = child.readline()
        print(x)
        if x == b'': break
        data += x
        if x.startswith(b'You are at '):
            print("We are there.")
            break
        if x.startswith(b'Pick her up?'):
            # By george I do!
            child.sendline('Y')
        #end if
    return data

def longest_path(io, first_node=0, last_node=9):
    """
    Input string
    Input first node integer starting point
    Input last node integer ending point (goal)
    Output list with the longest path.
    
    For example: itworks/lp0c_min.json the route it chose was: ['0', '7', '3', '4', '8', '4', '3', '2', '9']
    itworks/lp0d_min.json ['0', '1', '3', '6', '5', '6', '9']
    """
    global lp_filename_i
    io = io.replace('\r', '')
    links = [x.split(' -- ') for x in io.split('\n')]
    if len(links) <= 0: return []
    # FIXME: I don't know why this bug exists, but until it's fixed, we go this way.
    #links[-1].pop()
    nodes = set()
    for row in links:
        if len(row) < 2: continue
        nodes.update(row)
    print(nodes, links)
    if str(first_node) not in nodes or str(last_node) not in nodes:
        print("Error: missing {0} or {1}".format(first_node, last_node), sorted(list(nodes)))
        return []
    #end if
    map1 = Map([Point(name) for name in nodes])
    node_map = dict([(p.name, p) for p in map1.points])
    for row in links:
        if len(row) < 2: print("lonely row", row)
        for j in range(1, len(row)):
            if node_map[row[j]] in node_map[row[0]].conns: continue
            node_map[row[0]].addConn(node_map[row[j]])
        #next j
    #next row
    json_map = map1.saveJson()
    open('lp{0}.json'.format(lp_filename_i), 'w').write(json_map)
    lp_filename_i += 1
    start_node = node_map[str(first_node)]
    end_node = node_map[str(last_node)]
    shortest = map1.dijkstra(start_node, end_node)
    if None in shortest:
        print("No path", io)
        raise Exception("No path?")
    #end if
    r = [n.name for n in shortest]
    print('shortest path', shortest, r)
    if str(last_node) in r[:-1]: r = r[:r.index(str(last_node)) + 1]
    #print('r debug 2', r)
    # This won't find the longest path, but.. It might be a start.
    # What about dikstra?
    for c in nodes:
        # We already have 0 and 9 =]
        if c in [str(first_node), str(last_node)]: continue
        # We already have this one.
        if c in r: continue
        # Find a path from 0 to 9 through this path.
        r2 = map1.dijkstra(start_node, node_map[c])
        if r2 == None: continue
        if None in r2:
            print('r2 bug', 'lp{0}.json'.format(lp_filename_i-1), c)
            continue
        #end if
        r3 = map1.dijkstra(node_map[c], end_node)
        if r3 == None: continue
        if None in r3:
            print('r3 bug', 'lp{0}.json'.format(lp_filename_i-1), c)
            continue
        #end if
        r23 = r2[:-1] + r3
        r23 = [n.name for n in r23]
        # You can't go through 9 without going on to the next zone.
        if str(last_node) in r23[:-1]: r23 = r23[:r23.index(str(last_node)) + 1]
        if len(r23) > len(r):
            print("We actually found a longer route", r2, '--', r3)
            
            #print('r23 debug', [type(n) for n in r23])
            print('r23 debug 2', r23)
            r = r23[:]
        #end if
    #next c
    # You don't need to tell them to go to 0.
    if len(r) > 0 and r[0] == str(first_node): r.pop(0)
    return r
#end def longest_path(io, first_node=0, last_node=9)

#io = get_io().decode('utf-8')
#print(io)

io2 = get_io().decode('utf-8')
first_node = 0
last_node = 9
while True:
    io = io2
    if io == 'Next node: 9\r\n':
        print("you gotta be kidding me.")
        io = get_io().decode('utf-8')
    #end if
    if 'You are at' in io:
        endline = io.index('You are at')
        pos = io.index('. You want to get to ', endline + 1)
        first_node = int(io[endline+11:pos])
        pos2 = io.index('.', pos + 1)
        last_node = int(io[pos+21:pos2])
    #end if
    print(repr(io))
    r = longest_path(io, first_node, last_node)
    print('r', r)
    for v in r:
        print('sending', v)
        child.sendline(v)
        io2 = get_io().decode('utf-8')
        print(io2)
    #next v
    # No path, already an error
    if r == []: break
#loop

child.interact()
child = None
