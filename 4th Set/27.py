# Recover the key from CBC with IV=Key
# Take your code from the CBC exercise and modify it so that it repurposes the key for CBC encryption as the IV.

# Applications sometimes use the key as an IV on the auspices that both the 
# sender and the receiver have to know the key already, and can save some space by using it as both a key and an IV.

# Using the key as an IV is insecure; an attacker that can modify ciphertext 
# in flight can get the receiver to decrypt a value that will reveal the key.

# The CBC code from exercise 16 encrypts a URL string. Verify each byte of the 
# plaintext for ASCII compliance (ie, look for high-ASCII values). Noncompliant 
# messages should raise an exception or return an error that includes the decrypted 
# plaintext (this happens all the time in real systems, for what it's worth).

# Use your code to encrypt a message that is at least 3 blocks long:
# AES-CBC(P_1, P_2, P_3) -> C_1, C_2, C_3

# Modify the message (you are now the attacker):
# C_1, C_2, C_3 -> C_1, 0, C_1

# Decrypt the message (you are now the receiver) and raise the appropriate error if high-ASCII is found.

# As the attacker, recovering the plaintext from the error, extract the key:
# P'_1 XOR P'_3

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

	print plaintext
	print ''.join(plaintext)

	if ";admin=true;" in ''.join(plaintext):
		print 'you win'
	else:
		print 'you lose'

garbajo = vanilla("onononononon")
print "Before "+str(garbajo)
blah = "56040a195b53184642190c5041414141".decode("hex")
garbajo[2] = zor(blah,garbajo[2])
print "After "+str(garbajo)
ice(garbajo)

print 'ok\n\n\n'+":".join("{:02x}".format(ord(c)) for c in zor('ment2=%20lik',';admin=true;'))
