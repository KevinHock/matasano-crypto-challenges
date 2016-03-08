import time

import time
import random

# # Create a length 624 array to store the state of the generator
index = 0
mt = [None] * 624


# # Initialize the generator from a seed
def initialize_generator(seed):
    global index
    index = 0
    mt[0] = seed
    for i in xrange(1,624):
        moo = 1812433253 * (mt[i-1] ^ (mt[i-1] >> 30)) + i
        mt[i] = moo & 0xFFFFFFFF # 0x6c078965
        # print str(hex(mt[i]))

# initialize_generator(0)


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


# PART 1
# print 'current time is '
# while True:
# 	print int(time.time()) # making it easy

# now we guess through the limited range
# PART 2
output = 2918253533
output2 = 2326888331

# ENTER GUESS HERE 
guess = 1434641914

for estimate in xrange(guess,guess-1000000,-1):
	initialize_generator(estimate)
	if extract_number() == output:
		print 'WE CRACKED IT'
		print 'THE SEED IS '+str(estimate)
		if output2 != extract_number():
			print 'Just kidding, you suck'
		else:
			print 'fo real'
		break
	# else:
	# 	print ';('

# Output
# Yay
# WE CRACKED IT
# THE SEED IS 1434641908
# fo real







