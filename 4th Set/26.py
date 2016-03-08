import struct
import random
import os
from Crypto.Cipher import AES
import time

xtract_counter = 0
curr_xtract = [0,0,0,0]
index = 0
mt = [None] * 624
repeat = 0


# # Initialize the generator from a seed
def initialize_generator(seed):
    global index
    index = 0
    mt[0] = seed
    for i in xrange(1,624):
        moo = 1812433253 * (mt[i-1] ^ (mt[i-1] >> 30)) + i
        mt[i] = moo & 0xFFFFFFFF # 0x6c078965
        # print str(hex(mt[i]))

# # Generate an array of 624 untempered numbers
def generate_numbers():
    global index
    for i in xrange(0,623):
        # bit 31 (32nd bit) of mt[i]
         # bits 0-30 (first 31 bits) of mt[...]
        y = (mt[i] & 0x80000000) + (mt[(i+1) % 624] & 0x7fffffff)  
        mt[i] = mt[(i + 397) % 624] ^ (y >> 1)
        if (y % 2) != 0: # y is odd
            mt[i] = mt[i] ^ (2567483615) # 0x9908b0df

# # Extract a tempered pseudorandom number based on the index-th value,
# # calling generate_numbers() every 624 numbers
def extract_number():
    global index
    if index == 0:
        generate_numbers()
    
    y = mt[index]
    y = y ^ (y >> 11)
    y = y ^ ((y << 7) & (2636928640)) # 0x9d2c5680
    y = y ^ ((y << 15) & (4022730752)) # 0xefc60000
    y = y ^ (y >> 18)

    index = (index + 1) % 624
    return y

def get_byte():
	global xtract_counter
	global curr_xtract

	if xtract_counter % 4 == 0:
		torn = extract_number()
		# if __debug__:
			# print 'CHANGING curr_xtract'
		curr_xtract[0] = (torn >> (8*0)) & 0xFF
		curr_xtract[1] = (torn >> (8*1)) & 0xFF
		curr_xtract[2] = (torn >> (8*2)) & 0xFF
		curr_xtract[3] = (torn >> (8*3)) & 0xFF

	xtract_counter = (xtract_counter + 1) % 4
	
	# if __debug__:
		# print 'curr_xtract['+str(xtract_counter)+'] is '+str(hex(curr_xtract[xtract_counter]))

	return curr_xtract[xtract_counter]


def endecrypt(string, seed):
	global repeat
	global xtract_counter

	if repeat == 0:
		print 'string is '
		print ':'.join(x.encode('hex') for x in string)
	# else:
	# 	print '\n\nIn recursive_check'

	initialize_generator(seed)
	xtract_counter = 0

	result = ''

	for a in xrange(0,len(string)):
		# print 'Getting result'
		result = result + chr((ord(string[a]) ^ get_byte()))
		# print '---------------------------------'

	if repeat == 0:
		repeat = -1
		recursive_check = endecrypt(result, seed)
		print 'recursive_check is '
		print ':'.join(x.encode('hex') for x in recursive_check)

	return result

# CTR bitflipping
# There are people in the world that believe that CTR resists bit flipping attacks of the kind to which CBC mode is susceptible.

# Re-implement the CBC bitflipping exercise from earlier to use CTR mode instead of CBC mode. Inject an "admin=true" token.


def combine_and_eat(cookin):
	return endecrypt(("comment1=cooking%20MCs;userdata="+cookin+";comment2=%20like%20a%20pound%20of%20bacon").replace(";", "").replace("=", ""), 0xffff)

def decryption(ciphertext):
	plaintext = endecrypt(ciphertext, 0xffff)
	print plaintext
	print ':'.join(x.encode('hex') for x in plaintext)
	if ";admin=true;" in plaintext:
		print 'Aww yeah'
		print 'Aww yeah'
		print 'Aww yeah'

first_attempt = combine_and_eat("XadminXtrueX")
second_attempt = combine_and_eat("AadminAtrueA")
metachars = [i for i in xrange(len(first_attempt)) if first_attempt[i] != second_attempt[i]]

first_byte = ord(first_attempt[metachars[0]])^ord('X')^ord(';')
second_byte = ord(first_attempt[metachars[1]])^ord('X')^ord('=')
third_byte = ord(first_attempt[metachars[2]])^ord('X')^ord(';')

print 'len of metachars is '+str(len(metachars))
print 'metachars is'
print metachars
print 'first_attempt is'
print ':'.join(x.encode('hex') for x in first_attempt)
print 'first guess is'
geese = first_attempt[0:metachars[0]]+chr(first_byte)+first_attempt[metachars[0]+1:metachars[1]]+chr(second_byte)+first_attempt[metachars[1]+1:metachars[2]]+chr(third_byte)+first_attempt[metachars[2]+1:]
print ':'.join(x.encode('hex') for x in geese)
decryption(geese)
