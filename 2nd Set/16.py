# // ------------------------------------------------------------

# http://blog.gdssecurity.com/labs/2010/10/6/crypto-challenges-at-the-csaw-2010-application-ctf-qualifyin.html
# http://web.archive.org/web/20100528164302/http://chargen.matasano.com/chargen/2009/7/22/if-youre-typing-the-letters-a-e-s-into-your-code-youre-doing.html?
 
# 16. CBC bit flipping

import os
from Crypto.Cipher import AES

# Generate a random AES key.
key = 'YELLOW SUBMARINE' 

def zor(s1,s2):    
    # convert strings to a list of character pair tuples
    # go through each tuple, converting them to ASCII code (ord)
    # perform exclusive or on the ASCII code
    # then convert the result back to ASCII (chr)
    # merge the resulting array of characters as a string
    return ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(s1,s2))


# The first function should take an arbitrary input string, prepend the
# string:
#         "comment1=cooking%20MCs;userdata="
# and append the string:
#     ";comment2=%20like%20a%20pound%20of%20bacon"
# The function should quote out the ";" and "=" characters.
def vanilla(userdat):
	cookie = "comment1=cooking%20MCs;userdata="+userdat.replace(";","\";\"").replace("=","\"=\"")+";comment2=%20like%20a%20pound%20of%20bacon"
	padding = 16 - len(cookie) % 16
	print 'padding is '+str(padding)
	for i in range(0,padding):
		print 'i is '+str(i)

	# The function should then pad out the input to the 16-byte AES block
	# length and encrypt it under the random AES key.


	aees = AES.new(key, AES.MODE_ECB)

	for x in xrange(0,padding):
		cookie = cookie+chr(padding)	 
	
	# split plaintext up
	n = 16
	blocks = [cookie[i:i+n] for i in range(0, len(cookie), n)]

	print blocks

	# encrypt and chain
	ciphertext = []
	ciphertext.append(aees.encrypt(blocks[0]))

	print 'len of blocks is '+str(len(blocks))
	print blocks

	for x in xrange(1,len(blocks)):
		print 'xor '+str(x)+'th block with '+str(x+1)+'th block'
		breek = aees.encrypt(zor(blocks[x],ciphertext[x-1]))
		ciphertext.append(breek)
		print 'x+1 is '+str(x+1)
	return ciphertext
 	

# The second function should decrypt the string and look for the
# characters ";admin=true;" (or, equivalently, decrypt, split the string
# on ;, convert each resulting string into 2-tuples, and look for the
# "admin" tuple. Return true or false based on whether the string exists.
# If you've written the first function properly, it should not be
# possible to provide user input to it that will generate the string the
# second function is looking for.
def ice(ciphertext):
	print 'ciphertext is '+str(ciphertext)
	plaintext = []
	aees = AES.new(key, AES.MODE_ECB)
	
	# decrypt the first block
	print 'cipher[0]'+ciphertext[0]
	plaintext.append(aees.decrypt(ciphertext[0]))	
	print 'cipher[0]'+ciphertext[0]

	print '\nDecrypting\n'

	# decrypt the nth block then xor with the nth-1 block
	for x in xrange(1,len(ciphertext)-1):
		print 'x is '+str(x)+' x-1 '+str(x-1)
		print 'xor '+str(x-1)+'th block with decrypted '+str(x)+'th block'
		plaintext.append(zor(ciphertext[x-1],aees.decrypt(ciphertext[x])))
		# plaintext.append(zor(ciphertext[x-1],ciphertext[x-1]))

	print plaintext
	print ''.join(plaintext)

	if ";admin=true;" in ''.join(plaintext):
		print 'you win'
	else:
		print 'you lose'


# ice(vanilla("56040a195b53184642190c5041414141".decode("hex")))
garbajo = vanilla("onononononon")
print "Before "+str(garbajo)
# print garbajo[2]
blah = "56040a195b53184642190c5041414141".decode("hex")
garbajo[2] = zor(blah,garbajo[2])
# ice(vanilla("414141414141414141414141".decode("hex")))
print "After "+str(garbajo)
ice(garbajo)
# vanilla('helloeee')

print 'ok\n\n\n'+":".join("{:02x}".format(ord(c)) for c in zor('ment2=%20lik',';admin=true;'))

# Instead, modify the ciphertext (without knowledge of the AES key) to
# accomplish this.

# You're relying on the fact that in CBC mode, a 1-bit error in a
# ciphertext block:

# * Completely scrambles the block the error occurs in

# * Produces the identical 1-bit error (/edit) in the next ciphertext
#  block.

# Before you implement this attack, answer this question: why does CBC
# mode have this property?

# // ------------------------------------------------------------
# ':'.join(x.encode('hex') for x in 'Hello World!')