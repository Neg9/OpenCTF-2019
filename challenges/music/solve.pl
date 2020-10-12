#!/usr/bin/perl

use strict;
use warnings;
use feature 'say';
use File::Slurp;
use List::Util 'sum';

# sox music.flac -e float music.raw
#
my @samples = unpack('f*', read_file('music.raw'));
my @zero_crossings = (0);
my @notes;
for my $i (1 .. $#samples)
{
	if(($samples[$i - 1] > 0) != ($samples[$i] > 0))
	{
		if(@zero_crossings > 1)
		{
			my $dist = $i - $zero_crossings[-1];
			my $time = $i / 44100.0;
			my $freq = 44100.0 / $dist / 2.0;
			#printf "%2.8f %f\n", $time, $freq;
			push @{$notes[int($time/0.5)]}, $freq;
		}
		push @zero_crossings, $i;
	}
}

my %notes = (
	C0 => 16.35,
	D0 => 18.35,
	E0 => 20.60,
	F0 => 21.83,
	G0 => 24.50,
	A0 => 27.50,
	B0 => 30.87,
	C1 => 32.70,
	D1 => 36.71,
	E1 => 41.20,
	F1 => 43.65,
	G1 => 49.00,
	A1 => 55.00,
	B1 => 61.74,
	C2 => 65.41,
	D2 => 73.42,
	E2 => 82.41,
	F2 => 87.31,
	G2 => 98.00,
	A2 => 110.00,
	B2 => 123.47,
	C3 => 130.81,
	D3 => 146.83,
	E3 => 164.81,
	F3 => 174.61,
	G3 => 196.00,
	A3 => 220.00,
	B3 => 246.94,
	C4 => 261.63,
	D4 => 293.66,
	E4 => 329.63,
	F4 => 349.23,
	G4 => 392.00,
	A4 => 440.00,
	B4 => 493.88,
	C5 => 523.25,
	D5 => 587.33,
	E5 => 659.26,
	F5 => 698.46,
	G5 => 783.99,
	A5 => 880.00,
	B5 => 987.77,
	C6 => 1046.50,
	D6 => 1174.66,
	E6 => 1318.51,
	F6 => 1396.91,
	G6 => 1567.98,
	A6 => 1760.00,
	B6 => 1975.53,
	C7 => 2093.00,
	D7 => 2349.32,
	E7 => 2637.02,
	F7 => 2793.83,
	G7 => 3135.96,
	A7 => 3520.00,
	B7 => 3951.07,
	C8 => 4186.01,
	D8 => 4698.64,
);

my @detected_notes;
foreach my $note (@notes)
{
	my $avg_freq = sum(@$note) / @$note;
	my $detected_note = (sort { abs($avg_freq - $notes{$a}) <=> abs($avg_freq - $notes{$b}) } keys %notes)[0];
	say "$avg_freq $detected_note $notes{$detected_note}";
	push @detected_notes, $detected_note;
}

# 3      B4
# 3      D3
# 3      A3
# 4      C4
# 4      F3
# 5      F4
# 5      E4
# 6      B3
# 7      D4
# 7      G4
# 8      C5
# 9      D5
# 9      E3
# 14     G3
# 16     A4
# 17     C3

# 130.81 C3
# 146.83 D3
# 164.81 E3
# 174.61 F3
# 196 G3
# 220 A3
# 246.94 B3
# 261.63 C4
# 293.66 D4
# 329.63 E4
# 349.23 F4
# 392 G4
# 440 A4
# 493.88 B4
# 523.25 C5
# 587.33 D5

# convert the 16 distinct notes we've detected into 0-9A-F for hex
my %notes_to_hex = (
	C3 => '0',
	D3 => '1',
	E3 => '2',
	F3 => '3',
	G3 => '4',
	A3 => '5',
	B3 => '6',
	C4 => '7',
	D4 => '8',
	E4 => '9',
	F4 => 'a',
	G4 => 'b',
	A4 => 'c',
	B4 => 'd',
	C5 => 'e',
	D5 => 'f',
);

foreach my $detected_note (@detected_notes)
{
	print $notes_to_hex{$detected_note};
}
print "\n";
