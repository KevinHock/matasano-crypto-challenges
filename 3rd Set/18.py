import struct
from Crypto.Cipher import AES

NONCE_SIZE = 16
BLOCK_SIZE = 16

from binascii import unhexlify
import binascii

repeat = 0

def long_to_bytes (val, endianness='little'):
    """
    Use :ref:`string formatting` and :func:`~binascii.unhexlify` to
    convert ``val``, a :func:`long`, to a byte :func:`str`.

    :param long val: The value to pack

    :param str endianness: The endianness of the result. ``'big'`` for
      big-endian, ``'little'`` for little-endian.

    If you want byte- and word-ordering to differ, you're on your own.

    Using :ref:`string formatting` lets us use Python's C innards.
    """

    # one (1) hex digit per four (4) bits
    width = val.bit_length()

    # unhexlify wants an even multiple of eight (8) bits, but we don't
    # want more digits than we need (hence the ternary-ish 'or')
    # width += 8 - ((width % 8) or 8)
    width = 64

    # format width specifier: four (4) bits per hex digit
    fmt = '%%0%dx' % (width // 4)

    # prepend zero (0) to the width, to zero-pad the output
    s = unhexlify(fmt % val)

    if endianness == 'little':
        # see http://stackoverflow.com/a/931095/309233
        s = s[::-1]

    return s

def second(input_bytes, key, nonce):
	print 'IN SECOND'
	print 'IN SECOND'
	print 'IN SECOND'
	print 'IN SECOND'
	print 'IN SECOND'
	print 'IN SECOND'
	print 'IN SECOND'
	print 'IN SECOND'
	print 'IN SECOND'

	mode = AES.MODE_ECB

	aes = AES.new(key, mode, "0")
	# aes = AES.new(key, mode, nonce_64)
	plaintext = ""
	# input_bytes = bytearray(b"L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ==")
	print 'len of input_bytes is' +str(len(input_bytes))+' BOOM '
	print 'input_bytes ARE '+input_bytes
	for count in xrange(0,(len(input_bytes)/32)+1):
		if len(plaintext) == len(input_bytes):
			break
	
		count_64 = long_to_bytes(count,"little")
		nonce_64 = long_to_bytes(nonce,"little")
		nonce_cat_count = "%s%s" % (nonce_64, count_64)
		print 'nonce_cat_count is'
		print binascii.hexlify(nonce_cat_count)

		keystream = aes.encrypt(nonce_cat_count)
		print 'keystream is '+binascii.hexlify(keystream)

		# input ^ keystream
		for c in xrange(0,32,2):
			
			print 'input_bytes['+str(c)+'] is '+str(input_bytes[c-32+((count+1)*32)])+str(input_bytes[c+1-32+((count+1)*32)])


			print 'keystream['+str(c/2)+'] is '+binascii.hexlify(keystream[c/2])
			hmm = ((int(input_bytes[c-32+((count+1)*32)], 16)*16) + int (input_bytes[c+1-32+((count+1)*32)],16)) ^ ord(keystream[c/2])
			print 'hmm is '+str(hex(hmm))

			plaintext= plaintext + str('{:02x}'.format(hmm))
			if len(plaintext) == len(input_bytes):
				break
			print 'Now plaintext is '+plaintext

	print 'LEN OF 2ND input_bytes IS '+str(len(input_bytes))
	print 'LEN OF 2ND PLAINTEXT IS '+str(len(plaintext))

	return plaintext

def decrypt(string, key, nonce):
	global repeat

	nonce_64 = long_to_bytes(nonce,"little")

	mode = AES.MODE_ECB
	aes = AES.new(key, mode, "0")
	# aes = AES.new(key, mode, nonce_64)
	plaintext = ""
	# input_bytes = bytearray(b"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB")

	input_bytes = bytearray()
	input_bytes.extend(string)
	# print 'eeieieei input_bytes is'
	# print input_bytes

	# for count in xrange(0,len(string)/16):
	for count in xrange(0,(len(input_bytes)/16+1)):
		if len(plaintext) == len(input_bytes)*2:
			print 'breaking 110 b/c '+str(len(plaintext))
			break

		count_64 = long_to_bytes(count,"little")
		nonce_cat_count = "%s%s" % (nonce_64, count_64)
		print 'nonce_cat_count is'
		print binascii.hexlify(nonce_cat_count)

		keystream = aes.encrypt(nonce_cat_count)
		print 'keystream is '+binascii.hexlify(keystream)

		# input ^ keystream
		for c in xrange(0,16):
			print 'input_bytes[c-16+((count+1)*16)] is '+str(hex(input_bytes[c-16+((count+1)*16)]))
			print 'keystream[c] is '+binascii.hexlify(keystream[c])
			hmm = input_bytes[c-16+((count+1)*16)] ^ ord(keystream[c])
			print 'hmm is '+str(hex(hmm))

			print '@len(plaintext)/2 == len(input_bytes):'
			print 'len of plaintext is '+str(len(plaintext))
			print 'len of input_bytes is '+str(len(input_bytes))
			print '@len(plaintext)/2 == len(input_bytes):'
			print '@len(plaintext)/2 == len(input_bytes):'
			plaintext= plaintext + str('{:02x}'.format(hmm))
			if len(plaintext) == len(input_bytes)*2:
				print 'breaking 134 b/c '+str(len(plaintext))
				break
			print 'Now plaintext is '+plaintext
			
	print 'LEN OF 1ST input_bytes IS '+str(len(input_bytes))
	print 'LEN OF 1ST PLAINTEXT IS '+str(len(plaintext))
	print 'The first plaintext is '+plaintext

	asc_key = ''
	for x in xrange(0,len(plaintext),2):
		hmm = ((int(plaintext[x], 16)*16) + int (plaintext[x+1],16))
		asc_key = asc_key + str(chr(hmm))

	print 'asc_key is '+asc_key

	if repeat == 0:
		repeat = -1
		recursuve_check = decrypt(asc_key, key, nonce)
		print 'recursuve_check is '+str(recursuve_check)

	return asc_key
	# print 'ascii is '+(second(plaintext, key, nonce).decode("ascii"))
	# print 'ascii is '+binascii.b2a_hqx(second(plaintext, key, nonce))
	# print 'Last plaintext is '+second(plaintext, key, nonce)
	# print 'plaintext is '+second(plaintext, key, nonce)
	# print 'ascii is '+binascii.b2a_hqx(plaintext)
	# print 'ascii is '+plaintext.decode("ascii")

	# print '1ST trying it = '+plaintext#binascii.b2a_hqx(plaintext)


# string = "L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ=="
string = "booooooeiowierieowAALAAKAKAKAAKAKAKAAKKAKowAALAAKAKAKAAKAKAKAAKKAKAB"
nonce = 0
block_count = 0
key = "YELLOW SUBMARINE"

decrypt(string, key, nonce)

print '\n'