#!/usr/bin/env python3
"""
reverseRepr
by Javantea
April 16, 2011
Upgraded to python3 Feb 8, 2015
Added support for many complex types Feb 8, 2015
Additional support for tuples, dicts, and so forth added.

Reverse Repr is needed where you need to parse a file where you have written the output of repr().
I'm surprised that the docs actually recommend eval(). This is why we don't eval:
eval("\"test\" + "import os" + "os.system(just_imagine)" + \"\n")

If you use this to write a popular parser or language, please give credit to 
Javantea.

"""
from __future__ import print_function

escapes = {'t':'\t', 'r':'\r', 'n':'\n', '"':'"', '\\':'\\', "'":"'"}

def reverseRepr(data, returnEx = False, returnExtra=False):
	"""
	data is a string produced by repr
	if returnEx is set to True, the return is a tuple containing the output 
	and the length.
	"""
	#print("ends in pizza", data)
	if len(data) < 2:
		# No valid data could possibly be encoded as < 2 characters.
		return None
	#end if
	outputArray = False
	outputString = False
	outputDict = False
	outputTuple = False
	outputNumber = False
	outputNone = False
	outputBytes = False
	outputBool = False
	
	output = ''
	i = 0
	startChar = data[0]
	endItem = None
	endChar = None
	if startChar == '(':
		outputTuple = True
		endItem = ')'
		output = []
	elif startChar == '{':
		outputDict = True
		endItem = '}'
		output = {}
	elif startChar == '[':
		outputArray = True
		endItem = ']'
		output = []
	elif startChar == 'b':
		outputBytes = True
		outputString = True
		if len(data) < 2:
			# Error.
			return None
		#end if
		startChar = data[1]
		endChar = startChar
		endItem = startChar
	elif startChar == '"' or startChar == "'":
		outputString = True
		endChar = startChar
		endItem = startChar
	elif startChar in '0123456789':
		outputNumber = True
	elif startChar == 'N':
		outputNone = True
	elif startChar == 'T' or startChar == 'F':
		outputBool = True
	else:
		# Anything else is garbage
		if returnExtra: return data
		return None
	#end if
	
	if outputTuple or outputArray:
		# Parse an array by recursively parsing elements.
		x = 1
		while x < len(data):
			# Recursively add items.
			q = reverseRepr(data[x:], True)
			#print(q)
			if q == None or len(q) != 2:
				print("Error: reverseRepr recursion failed.", data[x:])
				break
			#end if
			output.append(q[0])
			x += q[1]
			#print('dx:', repr(data[x]))
			if x >= len(data): break
			if data[x] == ',':
				x += 1
			#end if
			if x >= len(data): break
			if data[x] == ' ':
				x += 1
			#end if
			if x >= len(data): break
			if data[x] == endItem:
				break
			#end if
		#loop
		
		if outputTuple:
			output = tuple(output)
		#end if
		#print('ter', output)
		if returnEx:
			return (output, x+1)
		#end if
		return output
	#end if
	
	if outputDict:
		# Parse a dict by recursively parsing elements.
		x = 1
		k = True
		v = False
		key = None
		while x < len(data):
			# Recursively add items.
			q = reverseRepr(data[x:], True)
			#print(q)
			if q == None or len(q) != 2:
				# Handle {} gracefully.
				if data[x] != '}':
					print("Error: reverseRepr recursion failed.", data[x:], data)
				#end if
				break
			#end if
			x += q[1]
			#print('dx:', repr(data[x]))
			if x >= len(data): break
			if data[x] == ':':
				#print('found key', q)
				key = q[0]
				x += 1
			#end if
			if data[x] == ',':
				#TODO:
				#if key == None: error
				#print('found value', q)
				output[key] = q[0]
				key = None
				x += 1
			#end if
			if x >= len(data): break
			if data[x] == ' ':
				x += 1
			#end if
			if x >= len(data): break
			if data[x] == endItem:
				#print('found value2', q)
				output[key] = q[0]
				break
			#end if
		#loop
		#print('yay', output)
		if returnEx:
			return (output, x+1)
		#end if
		return output
	#end if
	
	if outputNone:
		if data[:4] == 'None':
			if returnEx:
				return (None, 4)
			#end if
			return None
		#end if
		# An error occured if it gets here because nothing starts with 
		# N.
		return None
	#end if
	
	if outputBool:
		if data[:4] == 'True':
			if returnEx:
				return (True, 4)
			#end if
			return True
		#end if
		if data[:5] == 'False':
			if returnEx:
				return (False, 5)
			#end if
			return False
		#end if
		# An error occured if it gets here because nothing starts with 
		# N.
		return None
	#end if
	
	if outputNumber:
		# Parse an integer or a float.
		i = 0
		base = 10
		if data[:2] == '0x':
			i = 2
			base = 16
		#end if
		while i < len(data):
			if data[i] not in '0123456789.':
				break
			#end if
			output += data[i]
			i += 1
		#loop
		if '.' in output:
			# No 0x1.
			if base != 10: return None
			output = float(output)
		else:
			output = int(output, base)
		#end if
		if returnEx:
			return (output, i)
		#end if
		return output
	#end if
	
	# Parse a string or bytes.
	if outputBytes:
		output = b''
		i = 2
	else:
		i = 1
	#end if
	while i < len(data):
		if data[i] == '\\':
			# parse \
			if i+1 >= len(data):
				print('error parsing data at end', data[i:])
				return output
			#end if
			if data[i+1] == 'x':
				if i+3 >= len(data):
					print('error parsing data at end', data[i:])
					return output
				#end if
				# Next 2 are hex
				hexChar = data[i+2:i+4]
				if outputBytes == False:
					output += chr(int(hexChar, 16))
				else:
					output += bytes([int(hexChar, 16)])
				#end if
				i += 3
			elif data[i+1] in escapes:
				# tab \t, carraige return \r, line feed \n, quot ", apos ', backslash \ 
				if outputBytes:
					output += escapes[data[i+1]].encode('ascii')
				else:
					output += escapes[data[i+1]]
				#end if
				i += 1
			else:
				print("I don't know how to parse", repr(data[i+1]))
			#end if
		elif data[i] == endChar:
			if i == 0 or i == len(data) - 1:
				# These go away.
				pass
			else:
				break
			#end if
		else:
			if outputBytes:
				output += data[i].encode('utf-8')
			else:
				output += data[i]
			#end if
		#end if
		i += 1
	#loop
	
	if returnEx:
		return (output, i+1)
	else:
		return output
	#end if
#end def reverseRepr(data, outputType = 'string')

def main():
	a = ''.join([chr(a) for a in range(256)])
	# Success
	print(a == reverseRepr(repr(a)))
	print(repr(a) == repr(reverseRepr(repr(a))))
	# Here is repr
	print(repr(a))
	# Here is repr(b) where b is reversed from repr(a).
	print(repr(reverseRepr(repr(a))))
#end def main()


if __name__ == '__main__':
	main()
#end if
