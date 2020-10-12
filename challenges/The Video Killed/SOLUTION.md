1. Install gnuradio
2. Run "GNU Radio Command Prompt" if you are on Windows
3. navigate to the file with solution.py and challenge.bin
4. run "python solution.py"
5. You will be tuned into the radio station playing the flag.

challenge.bin is tuned into 0 on the slider of solution.py so real solvers will have to tune themselves.

solution.grc is a GNU Radio Companion file if you want to look at that.


## Setup

If you regenerate solution.py from solution.grc then please modify the file
path to be relative in the .py file.

If you use the "FM Encoder.grc" the destination file and the source file will 
have to be added. This grc is a bit complex because I was using it to experiment, 
There are essentiall two programs, a create and a solve, but you can connect the
two to test the sound without generating a file. If you do recreate challenge.bin
please do not loop the source recording, this keeps the file as small as possible.
And please try to have the radio playing something interesting.
