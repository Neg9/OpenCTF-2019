The desired user experience with this binary is that
people will run it before they take a look inside to 
see what it is doing. This will immediately kill their 
shell. 

After some very minor reversing you find out the binary 
reads 100 bytes from `/dev/urandom` and asks for the 
ones complement those bytes. 

The trick here is setting up pipes correctly. I ended up 
using a fifo and shell commands.
