#!/usr/bin/env python3
import time
import angr
import claripy

before = time.time()

binary = "./dist/tellme"
proj = angr.Project(binary)

start = claripy.BVV(b"flag{")
flag = claripy.BVS("flag", 16*8)
end = claripy.BVV(b"}\n")
flagsym = claripy.Concat(start, flag, end)

opts = angr.options.unicorn.union({"ZERO_FILL_UNCONSTRAINED_REGISTERS"})
state = proj.factory.full_init_state(
        args=[binary],
        add_options=opts,
        stdin=flagsym
)

for c in flag.chop(8):
    state.solver.add(c != 0)
    state.solver.add(c != ord("\n"))
    state.solver.add(c >= ord(" "))
    state.solver.add(c <= ord("~"))

simman = proj.factory.simulation_manager(state)
#simman.explore(find=lambda s: b"You got it!" in s.posix.dumps(1))
simman.explore(find=0x004014aa, avoid=[0x004014b8])
for s in simman.found:
    print(s.solver.eval(flagsym, cast_to=bytes))

after = time.time()
print("Time elapsed: {}".format(after - before))
