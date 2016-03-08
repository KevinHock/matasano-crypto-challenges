import base64
from binascii import unhexlify
import binascii
from Crypto.Cipher import AES
import sys

# Not needed foo
	# def hamstrings(str1, str2):
	# 	if len(str1) != len(str2):
	# 		print 'they aint equal foo'
	# 	# else:
	# 	# 	print "aww yeah they're equal"

	# 	# bits1 = binascii.a2b_base64(base64.b64encode(str1))
	# 	# bits2 = binascii.a2b_base64(base64.b64encode(str2))
		
	# 	# print 'bits1 is '+binascii.hexlify(bits1)
	# 	# print 'bits2 is '+binascii.hexlify(bits2)

	# 	bits1 = ''.join(format(ord(x), '8b') for x in str1)
	# 	bits2 = ''.join(format(ord(x), '8b') for x in str2)

	# 	total = 0
	# 	for x in xrange(0, len(bits2)):
	# 		if bits1[x]!=bits2[x]:
	# 			total = total + 1

	# 	print 'hammin is '+str(total)
	# 	print 'len(bits2) is '+str(len(bits2))

	# 	return total
	# dist = hamstrings("this is a test","wokka wokka!!!")

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

plaintexts =   [
"QUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFB",
				"SSdtIHJhdGVkICJSIi4uLnRoaXMgaXMgYSB3YXJuaW5nLCB5YSBiZXR0ZXIgdm9pZCAvIFBvZXRzIGFyZSBwYXJhbm9pZCwgREoncyBELXN0cm95ZWQ=",
				"Q3V6IEkgY2FtZSBiYWNrIHRvIGF0dGFjayBvdGhlcnMgaW4gc3BpdGUtIC8gU3RyaWtlIGxpa2UgbGlnaHRuaW4nLCBJdCdzIHF1aXRlIGZyaWdodGVuaW4nIQ==",
				"QnV0IGRvbid0IGJlIGFmcmFpZCBpbiB0aGUgZGFyaywgaW4gYSBwYXJrIC8gTm90IGEgc2NyZWFtIG9yIGEgY3J5LCBvciBhIGJhcmssIG1vcmUgbGlrZSBhIHNwYXJrOw==",
				"WWEgdHJlbWJsZSBsaWtlIGEgYWxjb2hvbGljLCBtdXNjbGVzIHRpZ2h0ZW4gdXAgLyBXaGF0J3MgdGhhdCwgbGlnaHRlbiB1cCEgWW91IHNlZSBhIHNpZ2h0IGJ1dA==",
				"U3VkZGVubHkgeW91IGZlZWwgbGlrZSB5b3VyIGluIGEgaG9ycm9yIGZsaWNrIC8gWW91IGdyYWIgeW91ciBoZWFydCB0aGVuIHdpc2ggZm9yIHRvbW9ycm93IHF1aWNrIQ==",
				"TXVzaWMncyB0aGUgY2x1ZSwgd2hlbiBJIGNvbWUgeW91ciB3YXJuZWQgLyBBcG9jYWx5cHNlIE5vdywgd2hlbiBJJ20gZG9uZSwgeWEgZ29uZSE=",
				"SGF2ZW4ndCB5b3UgZXZlciBoZWFyZCBvZiBhIE1DLW11cmRlcmVyPyAvIFRoaXMgaXMgdGhlIGRlYXRoIHBlbmFsdHksYW5kIEknbSBzZXJ2aW4nIGE=",
				"RGVhdGggd2lzaCwgc28gY29tZSBvbiwgc3RlcCB0byB0aGlzIC8gSHlzdGVyaWNhbCBpZGVhIGZvciBhIGx5cmljYWwgcHJvZmVzc2lvbmlzdCE=",
				"RnJpZGF5IHRoZSB0aGlydGVlbnRoLCB3YWxraW5nIGRvd24gRWxtIFN0cmVldCAvIFlvdSBjb21lIGluIG15IHJlYWxtIHlhIGdldCBiZWF0IQ==",
				"VGhpcyBpcyBvZmYgbGltaXRzLCBzbyB5b3VyIHZpc2lvbnMgYXJlIGJsdXJyeSAvIEFsbCB5YSBzZWUgaXMgdGhlIG1ldGVycyBhdCBhIHZvbHVtZQ==",
				"VGVycm9yIGluIHRoZSBzdHlsZXMsIG5ldmVyIGVycm9yLWZpbGVzIC8gSW5kZWVkIEknbSBrbm93bi15b3VyIGV4aWxlZCE=",
				"Rm9yIHRob3NlIHRoYXQgb3Bwb3NlIHRvIGJlIGxldmVsIG9yIG5leHQgdG8gdGhpcyAvIEkgYWluJ3QgYSBkZXZpbCBhbmQgdGhpcyBhaW4ndCB0aGUgRXhvcmNpc3Qh",
				"V29yc2UgdGhhbiBhIG5pZ2h0bWFyZSwgeW91IGRvbid0IGhhdmUgdG8gc2xlZXAgYSB3aW5rIC8gVGhlIHBhaW4ncyBhIG1pZ3JhaW5lIGV2ZXJ5IHRpbWUgeWEgdGhpbms=",
				"Rmxhc2hiYWNrcyBpbnRlcmZlcmUsIHlhIHN0YXJ0IHRvIGhlYXI6IC8gVGhlIFItQS1LLUktTSBpbiB5b3VyIGVhcjs=",
				"VGhlbiB0aGUgYmVhdCBpcyBoeXN0ZXJpY2FsIC8gVGhhdCBtYWtlcyBFcmljIGdvIGdldCBhIGF4IGFuZCBjaG9wcyB0aGUgd2Fjaw==",
				"U29vbiB0aGUgbHlyaWNhbCBmb3JtYXQgaXMgc3VwZXJpb3IgLyBGYWNlcyBvZiBkZWF0aCByZW1haW4=",
				"TUMncyBkZWNheWluZywgY3V6IHRoZXkgbmV2ZXIgc3RheWVkIC8gVGhlIHNjZW5lIG9mIGEgY3JpbWUgZXZlcnkgbmlnaHQgYXQgdGhlIHNob3c=",
				"VGhlIGZpZW5kIG9mIGEgcmh5bWUgb24gdGhlIG1pYyB0aGF0IHlvdSBrbm93IC8gSXQncyBvbmx5IG9uZSBjYXBhYmxlLCBicmVha3MtdGhlIHVuYnJlYWthYmxl",
				"TWVsb2RpZXMtdW5tYWthYmxlLCBwYXR0ZXJuLXVuZXNjYXBhYmxlIC8gQSBob3JuIGlmIHdhbnQgdGhlIHN0eWxlIEkgcG9zc2Vz",
				"SSBibGVzcyB0aGUgY2hpbGQsIHRoZSBlYXJ0aCwgdGhlIGdvZHMgYW5kIGJvbWIgdGhlIHJlc3QgLyBGb3IgdGhvc2UgdGhhdCBlbnZ5IGEgTUMgaXQgY2FuIGJl",
				"SGF6YXJkb3VzIHRvIHlvdXIgaGVhbHRoIHNvIGJlIGZyaWVuZGx5IC8gQSBtYXR0ZXIgb2YgbGlmZSBhbmQgZGVhdGgsIGp1c3QgbGlrZSBhIGV0Y2gtYS1za2V0Y2g=",
				"U2hha2UgJ3RpbGwgeW91ciBjbGVhciwgbWFrZSBpdCBkaXNhcHBlYXIsIG1ha2UgdGhlIG5leHQgLyBBZnRlciB0aGUgY2VyZW1vbnksIGxldCB0aGUgcmh5bWUgcmVzdCBpbiBwZWFjZQ==",
				"SWYgbm90LCBteSBzb3VsJ2xsIHJlbGVhc2UhIC8gVGhlIHNjZW5lIGlzIHJlY3JlYXRlZCwgcmVpbmNhcm5hdGVkLCB1cGRhdGVkLCBJJ20gZ2xhZCB5b3UgbWFkZSBpdA==",
				"Q3V6IHlvdXIgYWJvdXQgdG8gc2VlIGEgZGlzYXN0cm91cyBzaWdodCAvIEEgcGVyZm9ybWFuY2UgbmV2ZXIgYWdhaW4gcGVyZm9ybWVkIG9uIGEgbWljOg==",
				"THlyaWNzIG9mIGZ1cnkhIEEgZmVhcmlmaWVkIGZyZWVzdHlsZSEgLyBUaGUgIlIiIGlzIGluIHRoZSBob3VzZS10b28gbXVjaCB0ZW5zaW9uIQ==",
				"TWFrZSBzdXJlIHRoZSBzeXN0ZW0ncyBsb3VkIHdoZW4gSSBtZW50aW9uIC8gUGhyYXNlcyB0aGF0J3MgZmVhcnNvbWU=",
				"WW91IHdhbnQgdG8gaGVhciBzb21lIHNvdW5kcyB0aGF0IG5vdCBvbmx5IHBvdW5kcyBidXQgcGxlYXNlIHlvdXIgZWFyZHJ1bXM7IC8gSSBzaXQgYmFjayBhbmQgb2JzZXJ2ZSB0aGUgd2hvbGUgc2NlbmVyeQ==",
				"VGhlbiBub25jaGFsYW50bHkgdGVsbCB5b3Ugd2hhdCBpdCBtZWFuIHRvIG1lIC8gU3RyaWN0bHkgYnVzaW5lc3MgSSdtIHF1aWNrbHkgaW4gdGhpcyBtb29k",
				"QW5kIEkgZG9uJ3QgY2FyZSBpZiB0aGUgd2hvbGUgY3Jvd2QncyBhIHdpdG5lc3MhIC8gSSdtIGEgdGVhciB5b3UgYXBhcnQgYnV0IEknbSBhIHNwYXJlIHlvdSBhIGhlYXJ0",
				"UHJvZ3JhbSBpbnRvIHRoZSBzcGVlZCBvZiB0aGUgcmh5bWUsIHByZXBhcmUgdG8gc3RhcnQgLyBSaHl0aG0ncyBvdXQgb2YgdGhlIHJhZGl1cywgaW5zYW5lIGFzIHRoZSBjcmF6aWVzdA==",
				"TXVzaWNhbCBtYWRuZXNzIE1DIGV2ZXIgbWFkZSwgc2VlIGl0J3MgLyBOb3cgYW4gZW1lcmdlbmN5LCBvcGVuLWhlYXJ0IHN1cmdlcnk=",
				"T3BlbiB5b3VyIG1pbmQsIHlvdSB3aWxsIGZpbmQgZXZlcnkgd29yZCdsbCBiZSAvIEZ1cmllciB0aGFuIGV2ZXIsIEkgcmVtYWluIHRoZSBmdXJ0dXJl",
				"QmF0dGxlJ3MgdGVtcHRpbmcuLi53aGF0ZXZlciBzdWl0cyB5YSEgLyBGb3Igd29yZHMgdGhlIHNlbnRlbmNlLCB0aGVyZSdzIG5vIHJlc2VtYmxhbmNl",
				"WW91IHRoaW5rIHlvdSdyZSBydWZmZXIsIHRoZW4gc3VmZmVyIHRoZSBjb25zZXF1ZW5jZXMhIC8gSSdtIG5ldmVyIGR5aW5nLXRlcnJpZnlpbmcgcmVzdWx0cw==",
				"SSB3YWtlIHlhIHdpdGggaHVuZHJlZHMgb2YgdGhvdXNhbmRzIG9mIHZvbHRzIC8gTWljLXRvLW1vdXRoIHJlc3VzY2l0YXRpb24sIHJoeXRobSB3aXRoIHJhZGlhdGlvbg==",
				"Tm92b2NhaW4gZWFzZSB0aGUgcGFpbiBpdCBtaWdodCBzYXZlIGhpbSAvIElmIG5vdCwgRXJpYyBCLidzIHRoZSBqdWRnZSwgdGhlIGNyb3dkJ3MgdGhlIGp1cnk=",
				"WW8gUmFraW0sIHdoYXQncyB1cD8gLyBZbywgSSdtIGRvaW5nIHRoZSBrbm93bGVkZ2UsIEUuLCBtYW4gSSdtIHRyeWluZyB0byBnZXQgcGFpZCBpbiBmdWxs",
				"V2VsbCwgY2hlY2sgdGhpcyBvdXQsIHNpbmNlIE5vcmJ5IFdhbHRlcnMgaXMgb3VyIGFnZW5jeSwgcmlnaHQ/IC8gVHJ1ZQ==",
				"S2FyYSBMZXdpcyBpcyBvdXIgYWdlbnQsIHdvcmQgdXAgLyBaYWtpYSBhbmQgNHRoIGFuZCBCcm9hZHdheSBpcyBvdXIgcmVjb3JkIGNvbXBhbnksIGluZGVlZA==",
				"T2theSwgc28gd2hvIHdlIHJvbGxpbicgd2l0aCB0aGVuPyBXZSByb2xsaW4nIHdpdGggUnVzaCAvIE9mIFJ1c2h0b3duIE1hbmFnZW1lbnQ=",
				"Q2hlY2sgdGhpcyBvdXQsIHNpbmNlIHdlIHRhbGtpbmcgb3ZlciAvIFRoaXMgZGVmIGJlYXQgcmlnaHQgaGVyZSB0aGF0IEkgcHV0IHRvZ2V0aGVy",
				"SSB3YW5uYSBoZWFyIHNvbWUgb2YgdGhlbSBkZWYgcmh5bWVzLCB5b3Uga25vdyB3aGF0IEknbSBzYXlpbic/IC8gQW5kIHRvZ2V0aGVyLCB3ZSBjYW4gZ2V0IHBhaWQgaW4gZnVsbA==",
				"VGhpbmtpbicgb2YgYSBtYXN0ZXIgcGxhbiAvICdDdXogYWluJ3QgbnV0aGluJyBidXQgc3dlYXQgaW5zaWRlIG15IGhhbmQ=",
				"U28gSSBkaWcgaW50byBteSBwb2NrZXQsIGFsbCBteSBtb25leSBpcyBzcGVudCAvIFNvIEkgZGlnIGRlZXBlciBidXQgc3RpbGwgY29taW4nIHVwIHdpdGggbGludA==",
				"U28gSSBzdGFydCBteSBtaXNzaW9uLCBsZWF2ZSBteSByZXNpZGVuY2UgLyBUaGlua2luJyBob3cgY291bGQgSSBnZXQgc29tZSBkZWFkIHByZXNpZGVudHM=",
				"SSBuZWVkIG1vbmV5LCBJIHVzZWQgdG8gYmUgYSBzdGljay11cCBraWQgLyBTbyBJIHRoaW5rIG9mIGFsbCB0aGUgZGV2aW91cyB0aGluZ3MgSSBkaWQ=",
				"SSB1c2VkIHRvIHJvbGwgdXAsIHRoaXMgaXMgYSBob2xkIHVwLCBhaW4ndCBudXRoaW4nIGZ1bm55IC8gU3RvcCBzbWlsaW5nLCBiZSBzdGlsbCwgZG9uJ3QgbnV0aGluJyBtb3ZlIGJ1dCB0aGUgbW9uZXk=",
				"QnV0IG5vdyBJIGxlYXJuZWQgdG8gZWFybiAnY3V6IEknbSByaWdodGVvdXMgLyBJIGZlZWwgZ3JlYXQsIHNvIG1heWJlIEkgbWlnaHQganVzdA==",
				"U2VhcmNoIGZvciBhIG5pbmUgdG8gZml2ZSwgaWYgSSBzdHJpdmUgLyBUaGVuIG1heWJlIEknbGwgc3RheSBhbGl2ZQ==",
				"U28gSSB3YWxrIHVwIHRoZSBzdHJlZXQgd2hpc3RsaW4nIHRoaXMgLyBGZWVsaW4nIG91dCBvZiBwbGFjZSAnY3V6LCBtYW4sIGRvIEkgbWlzcw==",
				"QSBwZW4gYW5kIGEgcGFwZXIsIGEgc3RlcmVvLCBhIHRhcGUgb2YgLyBNZSBhbmQgRXJpYyBCLCBhbmQgYSBuaWNlIGJpZyBwbGF0ZSBvZg==",
				"RmlzaCwgd2hpY2ggaXMgbXkgZmF2b3JpdGUgZGlzaCAvIEJ1dCB3aXRob3V0IG5vIG1vbmV5IGl0J3Mgc3RpbGwgYSB3aXNo",
				"J0N1eiBJIGRvbid0IGxpa2UgdG8gZHJlYW0gYWJvdXQgZ2V0dGluJyBwYWlkIC8gU28gSSBkaWcgaW50byB0aGUgYm9va3Mgb2YgdGhlIHJoeW1lcyB0aGF0IEkgbWFkZQ==",
				"U28gbm93IHRvIHRlc3QgdG8gc2VlIGlmIEkgZ290IHB1bGwgLyBIaXQgdGhlIHN0dWRpbywgJ2N1eiBJJ20gcGFpZCBpbiBmdWxs",
				"UmFraW0sIGNoZWNrIHRoaXMgb3V0LCB5byAvIFlvdSBnbyB0byB5b3VyIGdpcmwgaG91c2UgYW5kIEknbGwgZ28gdG8gbWluZQ==",
				"J0NhdXNlIG15IGdpcmwgaXMgZGVmaW5pdGVseSBtYWQgLyAnQ2F1c2UgaXQgdG9vayB1cyB0b28gbG9uZyB0byBkbyB0aGlzIGFsYnVt",
				"WW8sIEkgaGVhciB3aGF0IHlvdSdyZSBzYXlpbmcgLyBTbyBsZXQncyBqdXN0IHB1bXAgdGhlIG11c2ljIHVw",
				"QW5kIGNvdW50IG91ciBtb25leSAvIFlvLCB3ZWxsIGNoZWNrIHRoaXMgb3V0LCB5byBFbGk=",
				"VHVybiBkb3duIHRoZSBiYXNzIGRvd24gLyBBbmQgbGV0IHRoZSBiZWF0IGp1c3Qga2VlcCBvbiByb2NraW4n",
				"QW5kIHdlIG91dHRhIGhlcmUgLyBZbywgd2hhdCBoYXBwZW5lZCB0byBwZWFjZT8gLyBQZWFjZQ=="]

def decrypt(string, key, nonce):
	global repeat
	
	nonce_64 = long_to_bytes(nonce,"little")

	mode = AES.MODE_ECB
	aes = AES.new(key, mode, "0")
	# aes = AES.new(key, mode, nonce_64)
	plaintext = ""
	input_bytes = bytearray()
	input_bytes.extend(string)

	# for count in xrange(0,len(string)/16):
	for count in xrange(0,(len(input_bytes)/16+1)):
		if len(plaintext) == len(input_bytes)*2:
			# print 'breaking 110 b/c '+str(len(plaintext))
			break

		count_64 = long_to_bytes(count,"little")
		nonce_cat_count = "%s%s" % (nonce_64, count_64)
		# print 'nonce_cat_count is'
		# print binascii.hexlify(nonce_cat_count)

		keystream = aes.encrypt(nonce_cat_count)
		# print 'keystream is '+binascii.hexlify(keystream)

		# input ^ keystream
		for c in xrange(0,16):
			# print 'input_bytes[c-16+((count+1)*16)] is '+str(hex(input_bytes[c-16+((count+1)*16)]))
			# print 'keystream[c] is '+binascii.hexlify(keystream[c])
			hmm = input_bytes[c-16+((count+1)*16)] ^ ord(keystream[c])
			# print 'hmm is '+str(hex(hmm))

			# print '@len(plaintext)/2 == len(input_bytes):'
			# print 'len of plaintext is '+str(len(plaintext))
			# print 'len of input_bytes is '+str(len(input_bytes))
			# print '@len(plaintext)/2 == len(input_bytes):'
			# print '@len(plaintext)/2 == len(input_bytes):'
			plaintext= plaintext + str('{:02x}'.format(hmm))
			if len(plaintext) == len(input_bytes)*2:
				# print 'breaking 134 b/c '+str(len(plaintext))
				break
			# print 'Now plaintext is '+plaintext
			
	# print 'LEN OF 1ST input_bytes IS '+str(len(input_bytes))
	# print 'LEN OF 1ST PLAINTEXT IS '+str(len(plaintext))
	# print 'The first plaintext is '+plaintext

	ass_key = ''
	for x in xrange(0,len(plaintext),2):
		hmm = ((int(plaintext[x], 16)*16) + int (plaintext[x+1],16))
		ass_key = ass_key + str(chr(hmm))

	# print 'ass_key is '+ass_key

	if repeat == 0:
		repeat = -1
		recursuve_check = decrypt(ass_key, key, nonce)
		# print 'recursuve_check is '+str(recursuve_check)

	return ass_key


ciphertexts = []
key = "YELLOW SUBMARINE"
nonce = 0

# Encrypt all the things
for x in xrange(0,len(plaintexts)):
	ciphertexts.append(base64.b64encode(decrypt(base64.b64decode(plaintexts[x]),key,nonce)))
	repeat = 0

# Find len_of_smallest
len_of_smallest = 1000000
for x in xrange(0,len(ciphertexts)):
	ciphertext = base64.b64decode(ciphertexts[x])
	if len_of_smallest > len(ciphertext):
		len_of_smallest = len(ciphertext)

# Create transposition
transposition = []
for x in xrange(0,len_of_smallest):
	transposition.append([])

# Fill transposition
for a in xrange(0,len(ciphertexts)):
	ciphertext = base64.b64decode(ciphertexts[a])
	for b in xrange(0,len_of_smallest):
		transposition[b].append(ciphertext[b])

# Do letter frequency analysis
chars = "eE tTaAoOiInNsShHrRdDlLcCuUmMwWfFgGyYpPbBvVkKjJxXqQzZ'";
freqs = [13,13, 10, 9,9, 8,8, 7,7, 7,7, 7,7, 6,6, 6,6, 6,6, 4,4, 4,4, 3,3, 3,3, 3,3, 2,2, 2,2, 2,2, 2,2, 2,2, 1,1, 1,1, 1,1, 0,0, 0,0, 0,0, 0,0,0];

keys = []
total = 0
best_total_so_far = 0

correct_WTF = ''
huhwtf = ''
# for a in xrange(0,len_of_smallest):
for a in xrange(0,len_of_smallest):
	print 'ROUND '+str(a)+": FIGHT\n\n\n"
	# print 'transposition[a] is '
	# print transposition[a]

	best_total_so_far = 0
	best_key_so_far = -1


	for key in xrange(0,256):
		total = 0

		for b in xrange(0,len(ciphertexts)):
		
			# print 'current is '+str(transposition[a][b])
			# print 'as a number '+str(ord(transposition[a][b]))

			hmm = ord(transposition[a][b])
			# huhwtf = ''
			# Test possible keys
				# print 'key^current is '+str(hex((ord(transposition[a][b])^key))) 

			if key == 0x7f:
				huhwtf = huhwtf + chr(hmm^key)
			if key == 0x76:
				correct_WTF = correct_WTF + chr(hmm^key)

			checkie = 1
			# Check with English letters
			for d in xrange(0,len(chars)):

				if hmm^key == ord(chars[d]):
					# print 'BALLIN'
					# print 'BALLIN'
					# print 'BALLIN'
					# print 'BALLIN'
					# print 'BALLIN'
					checkie = 0
					total = total + freqs[d]
			if checkie == 1:
				total = total -15			
		if best_total_so_far <= total:
			best_total_so_far = total
			best_key_so_far = key
			print 'best_total_so_far is '+str(hex(best_total_so_far))
			print 'best_key_so_far is '+str(hex(best_key_so_far))
			stir = ''
			for q in xrange(0,len(ciphertexts)):
				stir = stir + chr(ord(transposition[a][q])^best_key_so_far)
			print 'stir is '+stir
		if key == 0x76:
			print 'CORRECT total is '+str(hex(total))
			stir = ''
			for q in xrange(0,len(ciphertexts)):
				stir = stir + chr(ord(transposition[a][q])^118)
			print 'CORRECT stir is '+stir


	keys.append(best_key_so_far)

print 'keys '
for x in xrange(0,len(keys)):
	print hex(keys[x])

print 'should be keystream is 76d1cb4bafa246e2e3af035d6c13c372 d2ec6cdc986d12decfda1f93afee7318'

# for d in xrange(0,len(chars)):
# 	if 101 == ord(chars[d]):
# 		print 'e motherfucker'


# idk = 0x76
# bop = ord(transposition[0][0])

# print 'should be 0x41 is '+str(hex(bop^idk))


# print 'correct_WTF is '+correct_WTF
# print 'huhwtf is '+huhwtf

print 'THE CLEARTEXT'
print 'THE CLEARTEXT'
print 'THE CLEARTEXT'
print 'THE CLEARTEXT'
print 'THE CLEARTEXT'
print 'THE CLEARTEXT'
print 'THE CLEARTEXT'
print 'THE CLEARTEXT'
print 'THE CLEARTEXT'

for a in xrange(0,len_of_smallest):
# for a in xrange(0,1):
	for b in xrange(0,len(keys)):
		sys.stdout.write(chr(ord(transposition[b][a]) ^ keys[b]))
	print ''

