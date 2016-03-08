import base64
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

# print extract_number()


# Write a routine that performs the following operation:

# Wait a random number of seconds between, I don't know, 40 and 1000.
# Seeds the RNG with the current Unix timestamp
# Waits a random number of seconds again.
# Returns the first 32 bit output of the RNG.

# From the 32 bit RNG output, discover the seed.

random.seed()

print 'ghi'

def coffee():
	time.sleep(random.randrange(40,80))
	seed = int(time.time()) # needs to be int fo the functs to work,
	initialize_generator(seed)
	time.sleep(random.randrange(40,80))
	print extract_number()
	print extract_number()
	print 'seed was '+str(base64.b64encode(str(seed)))
	print '---------------------------'

while True:
	coffee()




























