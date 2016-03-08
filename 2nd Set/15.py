# b4cbday and just got momentum
# // ------------------------------------------------------------

# 15. PKCS#7 padding validation

# Write a function that takes a plaintext, determines if it has valid
# PKCS#7 padding, and strips the padding off.

# The string:

#     "ICE ICE BABY\x04\x04\x04\x04"

# has valid padding, and produces the result "ICE ICE BABY".

# The string:

#     "ICE ICE BABY\x05\x05\x05\x05"

# does not have valid padding, nor does:

#      "ICE ICE BABY\x01\x02\x03\x04"

# If you are writing in a language with exceptions, like Python or Ruby,
# make your function throw an exception on bad padding.

# // ------------------------------------------------------------


def valid_padding(test):
	try:
		n = len(test)
		pad = int(test[-1:].encode('hex') , 16)
		print 'n   - len should be '+str(n)
		print 'pad - nth should be '+str(pad)

		for i in range(0, pad):
			p1 = n-pad+i
			print 'test[p] is'+str(int(test[p1].encode('hex'), 16))
			value = int(test[p1].encode('hex'), 16)

			if value is pad:
				print "Good so far."
			else:
				raise Exception()
		return 1
		pass
	except Exception, e:
		print 'Bad padding.'
		raise e
		return 0

valid_padding("ICE ICE BABY\x04\x04\x04\x04")
print 'should be one:'+str(valid_padding("ICE ICE BABY\x04\x04\x04\x04"))
print 'should be zero:'+str(valid_padding("ICE ICE BABYyoyo\x10\x10\x10\x10\x10\x18\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10"))
print 'should be zero:'+str(valid_padding("ICE ICE BABY\x05\x05\x05\x05"))
