Challenge provides a flac file that when listened to sounds like a bunch of random notes. It can be observed that the notes change every 0.5 seconds. Players analyze the audio through whatever means they can to extract the notes. The solve.pl that I wrote uses zero crossings to determine frequencies, and looking at the frequencies, it is obvious that they fall in buckets which I mapped to standard notes' frequences. When doing so, it can be observed that only 16 distinct notes are used throughout the audio. Mapping each note to 0-9A-F gives a hex string that, when converted to binary, clearly contains a portion that says "flag.txt" as an indication that you're on the right track. Saving this binary to a file and running `file` on it gives:

```test: gzip compressed data, was "flag.txt", last modified: Tue Jan 22 06:54:45 2019, from Unix, original size 31```

Running `zcat` on the binary file provides the flag.

=====
The solve.pl script I wrote to confirm the challenge works relies on the perl module File::Slurp. All other dependencies should be base perl modules.

The solve.pl script takes a raw floating point pcm of the flac file, converted with:
sox music.flac -e float music.raw


```
$ sudo apt install sox
$ sudo cpan install File::Slurp
$ sox dist/music.flac -e float music.raw


$ ipython 
In [1]: s = "1f8b080835be465c0003666c61672e747874004bcb494caf2ece2fcd4b298e4fcc4daccacc4b8f4fc94f2dce2b89cf2ca9e50200a43e04321f000000"
In [3]: f = open('foo','wb')
In [4]: f.write(s.decode('hex'))
In [5]: f.close()


$ zcat ~/foo

```

