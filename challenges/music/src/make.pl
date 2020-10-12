#!/usr/bin/perl

use strict;
use warnings;
use diagnostics;
use feature 'say';
use Data::Dumper;
use File::Slurp 'slurp';
use POSIX 'fmod';

my $samplerate = 44100;


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

# CONSTANTS
my @mapping = qw(C3 D3 E3 F3 G3 A3 B3 C4 D4 E4 F4 G4 A4 B4 C5 D5);
my $volume = 0.8;
my $note_duration = 0.5;
use constant PI => 3.14159265359;

my $sample_num = 0;
my $done = 0;


my $data = slurp('flag.txt.gz');
my @data = split //, unpack('H*', $data);
print Dumper(\@data);

my $freq;
my $phase_shift = 0;
my $previous_phase = 0;
my $next_note_sample = 0;

open RAW, ">music.raw";
while(1)
{
	last unless (@data);
	$freq = $notes{$mapping[hex(shift @data)]};
	$phase_shift = fmod($previous_phase, 2 * PI);

	foreach my $sample_num (0 .. $samplerate / 2 - 1)
	{
		my $phase = 2 * PI * $freq * $sample_num / $samplerate + $phase_shift;
		my $amp = $volume * sin($phase);

		$previous_phase = $phase;
		print RAW pack('f', $amp);
	}
}

`sox --encoding floating-point --bits 32 -r 44100 music.raw music.flac`;
