morseAlphabet ={
      "A" : ".-",
      "B" : "-...",
      "C" : "-.-.",
      "D" : "-..",
      "E" : ".",
      "F" : "..-.",
      "G" : "--.",
      "H" : "....",
      "I" : "..",
      "J" : ".---",
      "K" : "-.-",
      "L" : ".-..",
      "M" : "--",
      "N" : "-.",
      "O" : "---",
      "P" : ".--.",
      "Q" : "--.-",
      "R" : ".-.",
      "S" : "...",
      "T" : "-",
      "U" : "..-",
      "V" : "...-",
      "W" : ".--",
      "X" : "-..-",
      "Y" : "-.--",
      "Z" : "--..",
      " " : " ",
      "_" : "..--.-",
      "0" : "-----",
      "1" : ".----",
      "2" : "..---",
      "3" : "...--",
      "4" : "....-",
      "5" : ".....",
      "6" : "-....",
      "7" : "--...",
      "8" : "---..",
      "9" : "----.",
      }

inverseMorseAlphabet=dict((v,k) for (k,v) in morseAlphabet.items())


testCode = ".... . .-.. .-.. --- / -.. .- .. .-.. -.-- / .--. .-. --- --. .-. .- -- -- . .-. / --. --- --- -.. / .-.. ..- -.-. -.- / --- -. / - .... . / -.-. .... .- .-.. .-.. . -. --. . ... / - --- -.. .- -.-- "

# parse a morse code string positionInString is the starting point for decoding
def decodeMorse(code, positionInString = 0):

   if positionInString < len(code):
      morseLetter = ""
      for key,char in enumerate(code[positionInString:]):
	 if char == " ":
	    positionInString = key + positionInString + 1
	    letter = inverseMorseAlphabet[morseLetter]
	    return letter + decodeMorse(code, positionInString)

	 else:
	    morseLetter += char
   else:
      return ""

#encode a message in morse code, spaces between words are represented by '/'
def encodeToMorse(message):
   encodedMessage = ""
   for char in message[:]:
      encodedMessage += morseAlphabet[char.upper()] + " "

   return encodedMessage




if __name__=='__main__':
   s = encodeToMorse('N3V3R_SEND_A_B0Y_7O_D0_A_W0MAN5_JOB')
   print s
   print decodeMorse(s)

   clist = []
   for w in s.split():
      for c in w:
	 if c == '.':
	    clist.append("dit();")
	 elif c == '-':
	    clist.append("dah();")
      clist.append("delay(3*GAP);\n")

   print " ".join(clist)
