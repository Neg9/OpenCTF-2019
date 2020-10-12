This is a dungeon crawler which has a chest on the lowest level.
When opening the chest it takes the flag string, hashes it with md5, and
compares it to a static checksum of the string that's stored in the binary.

The trick is finding actually finding the md5 checksum in the binary, which is
a bit tricker in golang since strings aren't null terminated.

There are some IDA plugins to help reverse go binaries. We can use one of two
plugins to recreate the function names and strings in IDA Pro for golang:
* <https://github.com/strazzere/golang_loader_assist>
* <https://github.com/sibears/IDAGolangHelper>

Then we can see the `main_open()` function which unlocks the chest.
Seeing that it takes an md5sum of the input, and compares to a string, we pull
that string out, throw it in hashcat, and get the flag.
