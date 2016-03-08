import struct
import random
import os
from Crypto.Cipher import AES
import time


# # Create a length 624 array to store the state of the generator
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










# You can create a trivial stream cipher out of any PRNG; use it to generate 
# a sequence of 8 bit outputs and call those outputs a keystream. XOR each byte 
# of plaintext with each successive byte of keystream.

# # Write the function that does this for MT19937 using a 16-bit seed. Verify 
# that you can encrypt and decrypt properly. This code should look similar to your CTR code.
# PART 1

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

# result = endecrypt("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", 0xffff)
# print 'result is '
# print ':'.join(x.encode('hex') for x in result)



































# # Use your function to encrypt a known plaintext (say, 14 consecutive 'A' characters) 
# prefixed by a random number of random characters.

# From the ciphertext, recover the "key" (the 16 bit seed).
# PART 2

known_plaintext = 'AAAAAAAAAAAAAA'
plaintext = ''

random.seed()
num = random.randrange(0,80)

for x in xrange(0,int(num)):
	plaintext = plaintext + chr(random.randrange(0,255))
plaintext = plaintext + known_plaintext

# print 'plaintext is '
# print ':'.join(x.encode('hex') for x in plaintext)

repeat = -1
ciphertext = endecrypt(plaintext, 0xffff)


# for x in xrange(0,0x10000):
# 	if plaintext == endecrypt(ciphertext, x):
# 		print 'We brokes it!'







































# Use the same idea to generate a random "password reset token" 
# using MT19937 seeded from the current time.

def dar_know_what_time_it_is(ciphertext):
	curr_time = int(time.time())
	zeroes = ''
	for x in xrange(0,len(ciphertext)):
		zeroes = zeroes + '\x00'
	for a in xrange(curr_time,curr_time-500, -1):
		prng_output = endecrypt(zeroes, curr_time)
		plaintext_of_token = ''
		for b in xrange(0,len(ciphertext)):
			plaintext_of_token = plaintext_of_token + chr(ord(prng_output[b]) ^ ord((ciphertext[b])))
		guess = endecrypt(plaintext_of_token, a)
		if guess == ciphertext:
			print 'Aww yeah'
			return True
	return False

# Write a function to check if any given password token is actually 
# the product of an MT19937 PRNG seeded with the current time.
# PART 3


ciphertext = endecrypt(plaintext, int(time.time()))

dar_know_what_time_it_is(ciphertext)


