import socket
import binascii

HOST = "fake"
PORT = 12345

s = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

solved_plaintext = "}"
for loopdloop in xrange(0,13):
	for guess in xrange(1,256):
		chosen_plaintext = ""
		chosen_plaintext += str(chr(guess))
		chosen_plaintext += solved_plaintext[::-1]
		for i in xrange(0,15-len(solved_plaintext)):
			chosen_plaintext += "\x00"
		chosen_plaintext += solved_plaintext
		chosen_plaintext += "ABCD\n"
		# print binascii.hexlify(bytearray(chosen_plaintext))
		s.send(chosen_plaintext)
		ciphertext = s.recv(1024)
		if len(ciphertext) != 96:
			print "ciphertext len (should be 96) is "+str(len(ciphertext))
			break
		blocks_of_ciphertext = [ciphertext[i:i+32] for i in range(0, len(ciphertext), 32)]
		if blocks_of_ciphertext[0] == blocks_of_ciphertext[2]:
			print "blocks_of_ciphertext is "
			print blocks_of_ciphertext
			print "Got solved_plaintext["+str(len(solved_plaintext))+"]"
			solved_plaintext += str(chr(guess))
			print "the characters value is "+str(guess)
			print "solved_plaintext is "+solved_plaintext[::-1]
s.close()
