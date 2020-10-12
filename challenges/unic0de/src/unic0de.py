#!/usr/bin/env python3
"""
Unic0de in a Nutshell
by Javantea
Sept 27, 2017

I'm finally going to release a set of unicode junk that will help pentesters.
"""
import re
import string
import random
import binascii

# this character doesn't like you typing before it. Most don't.
x  = '𝐟'

fraktur_s = '𝔖'
converts_to_ascii = '𝗣𝗮𝘆𝗽𝗮𝗹'

poopfire = '💩🔥'

dark_modifier = '🏿'
santa = '🎅'
dark_santa = santa + dark_modifier
shining_star = '🌟'
dark_star = shining_star + dark_modifier
kavirama = 'क्'
kaviramazwj = 'क्‍'
kaviramasa = 'क्ष'
kaviramazwjsa = 'क्‍ष'
raviramaka = 'ರ್ಕ'
razwjviramaka = 'ರ‍್ಕ'

Naviramazwj = 'ണ്‍'
naviramazwj = 'ന്‍'

copyleft = '🄯'
copyleft2 = 'ↄ⃝'

superhero = '🦸'
teddybear = '🧸'
lobster = '🦞'
man = '👨'
medium = '🏽‍'
red = '🦰'
man_medium_red = man + medium + red
man_medium_red2 = man + red + medium
labcoat = '🥼'
raccoon = '🦝'
swan = '🦢'
microbe = '🦠'
skateboard = '🛹'
nazar = '🧿'
dna = '🧬'
infinity = '♾'
pirateflag = '🏴‍☠️'
vulcan_salute = '🖖'
man_suit_levitating = '🕴️'
facepalm = '🤦'
info = 'ℹ️'
thechain = '⛓️'
cyclist = '🚴'
woman = '👩‍'
zwj_man_kiss_man = man + '❤️‍💋‍' + man
zwj_man_kiss_woman = man + '❤️‍💋‍' + woman
zwj_man_kiss_superhero = man + '❤️‍💋‍' + superhero
zwj_woman_kiss_woman = woman + '❤️‍💋‍' + woman
zwj_woman_kiss_man = woman + '❤️‍💋‍' + man
zwj_superhero_kiss_woman = superhero + '❤️‍💋‍' + woman
zwj_woman_heart_woman = woman + '❤️‍' + woman

ogham1 = '᚛ᚈᚑᚋ ᚄᚉᚑᚈᚈ᚜'
ogham2 = '᚛ᚑᚌᚐᚋ᚜'

cherokee = ''
for i in range(0xe18ea0, 0xe18fbe):
	try:
		cherokee += binascii.unhexlify(hex(i)[2:]).decode('utf-8')
	except UnicodeDecodeError:
		print(i)
	#end try
#next i
if cherokee != 'ᎠᎡᎢᎣᎤᎥᎦᎧᎨᎩᎪᎫᎬᎭᎮᎯᎰᎱᎲᎳᎴᎵᎶᎷᎸᎹᎺᎻᎼᎽᎾᎿᏀᏁᏂᏃᏄᏅᏆᏇᏈᏉᏊᏋᏌᏍᏎᏏᏐᏑᏒᏓᏔᏕᏖᏗᏘᏙᏚᏛᏜᏝᏞᏟᏠᏡᏢᏣᏤᏥᏦᏧᏨᏩᏪᏫᏬᏭᏮᏯᏰᏱᏲᏳᏴᏵ\u13f6\u13f7ᏸᏹᏺᏻᏼᏽ':
	print("Warning: Cherokee changed since this program was written.")
#end if
cherokee_unknown = '\u13f6\u13f7'
#print(cherokee)
#len(cherokee)
#94

canadian_ai = 'ᐜ'
canadian_other = 'ᐝᐞᐟᐠᐡᐢᐣᐤᐥᐦᐧᐨᐩᐪ'

runic_unprintable = '\u16f1\u16f2\u16f3\u16f4\u16f5\u16f6\u16f7\u16f8'

khmer_overwrite = 'a៑៑b៍c៌d់e៊f៉gំhួiូjុ'

def unic0de(length):
	return [chr(x) for x in range(length)]

def preUnic0de(s, length):
	return unic0de(length) + s
#end def preUnic0de(s, length)

def unic0de_r():
	junk = [b'\xcc'.decode('utf-8','replace'), x, fraktur_s, converts_to_ascii, poopfire, dark_modifier, santa, dark_santa, shining_star, dark_star, kavirama, kaviramazwj, kaviramasa, kaviramazwjsa, raviramaka, razwjviramaka, Naviramazwj, naviramazwj, copyleft, copyleft2, superhero, teddybear, lobster, man, medium, red, man_medium_red, man_medium_red2, labcoat, raccoon, swan, microbe, skateboard, nazar, dna, infinity, pirateflag, vulcan_salute, man_suit_levitating, facepalm, info, thechain, cyclist, woman, zwj_man_kiss_man, zwj_man_kiss_woman, zwj_man_kiss_superhero, zwj_woman_kiss_woman, zwj_woman_kiss_man, zwj_superhero_kiss_woman, zwj_woman_heart_woman, ogham1, ogham2, cherokee_unknown, canadian_ai, canadian_other, runic_unprintable]
	unic0de_add = []
	for v in junk:
		for w in junk:
			unic0de_add.append(v+w)
		#next w
	#next v
	unic0de_static = junk + unic0de_add

	junk = unic0de_static + unic0de(10000)
	unic0de_add = []
	for v in junk:
		if random.randint(0, 34) == 0:
			for w in junk:
				if random.randint(0, 54) == 0:
					unic0de_add.append(v+w)
				#end if
			#next w
		#end if
	#next v
	return junk + unic0de_add
	#print(len(unic0de_r))
	#61799

"""
print(b+b+b)
ൢൢൢ

print(b+b+b+'<script>alert(1);</script>'+b+b+b)
ൢൢൢ<script>alert(1);</script>ൢൢൢ

"""

# A list of characters that are delimiters.

#b'\xcc'.decode('utf-8','replace')
#'�'
#_.encode('utf-8')
#b'\xef\xbf\xbd'

# utf-8 doesn't use printable characters except ?. When is ? a delimiter? Urls. Sentences.

#e = [re.findall(re.escape(x.encode('utf-8')), d) for x in string.printable]      

def main():
	a = unic0de(100000)

	print('unic0de_r is', len(unic0de_r()))
#end def main()

if __name__ == '__main__':
	main()
#end if
