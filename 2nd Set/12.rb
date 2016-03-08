require "base64"
require "openssl"
require "SecureRandom"

$final_message = Array.new()
$key = SecureRandom.random_bytes(16)
secret = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"

# The day I wrote my first Ruby function 8/21/13
def encrypt(input)
	cipher = OpenSSL::Cipher::AES.new(128, :ECB)
	cipher.encrypt
	cipher.key = $key
	result = cipher.update(input) + cipher.final
	return result
end



# a. Feed identical bytes of your-string to the function 1 at a time ---
# start with 1 byte ("A"), then "AA", then "AAA" and so on. Discover the
# block size of the cipher. You know it, but do this step anyway.
plaintext = "A"
got_neither = 0
got_one = 0
got_second = 0

for find_blocksize in 0..50
	input = plaintext + Base64.decode64(secret)
	output = encrypt(input)
	if got_neither == 0
		got_neither = output.length
	end
	if got_neither != output.length and got_one == 0
		got_one = output.length
	end
	if got_one != output.length and got_one != 0
		got_second = output.length
		break
	end
	plaintext << "A"
end	

ablock_size = got_second.to_i-got_one.to_i
puts "Block size is #{ablock_size}"



# b. Detect that the function is using ECB. You already know, but do
# this step anyways.
# DETECT ECB OR CBC BY USING #8 MOSTLY
bi=0
binput = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" + Base64.decode64(secret)
boutput = encrypt(binput)
crypted_blocks = boutput.scan(/.{16}/)

crypted_blocks.each_with_index do |element,index|
  		for element in crypted_blocks do
		  if crypted_blocks[index] == element
		  	bi=bi+1
		  end
		end
	end

if bi == crypted_blocks.length
	puts "CBC"
else
	puts "ECB"
end



# c. Knowing the block size, craft an input block that is exactly 1 byte
# short (for instance, if the block size is 8 bytes, make
# "AAAAAAA"). Think about what the oracle function is going to put in
# that last byte position.
# d. Make a dictionary of every possible last byte by feeding different
# strings to the oracle; for instance, "AAAAAAAA", "AAAAAAAB",
# "AAAAAAAC", remembering the first block of each invocation.

ecb_dictionary = Array.new()

for ci in 1..126
	#         123456789012345
	cinput = "AAAAAAAAAAAAAAA" + ci.chr
	ecb_dictionary.push(encrypt(cinput))
end
	
puts ecb_dictionary[0].length



# e. Match the output of the one-byte-short input to one of the entries
# in your dictionary. You've now discovered the first byte of
# unknown-string.

#         123456789012345
einput = "AAAAAAAAAAAAAAA" + Base64.decode64(secret)
eoutput = encrypt(einput)
ecrypted_blocks = eoutput.scan(/.{32}/)
maybe = ecrypted_blocks[0].scan(/.{16}/)

for ei in 1..126
	solo = ecb_dictionary[ei-1].scan(/.{16}/)
	if maybe[0] == solo[0]
		$final_message.push(ei.chr)
	end
end



# f. Repeat for the next byte.
secret = Base64.decode64(secret)

fi = secret.length
for ilovematasano in 0..fi-2
	secret = secret[1..-1]
	#         123456789012345
	zinput = "AAAAAAAAAAAAAAA" + secret.chars.first
	zoutput = encrypt(zinput)
	maybez = zoutput.scan(/.{16}/)

	for findits in 0..126
		test = ecb_dictionary[findits-1]
		soloz = test.scan(/.{16}/)
		if maybez[0] == soloz[0]
			$final_message.push(findits.chr)
		end
	end
end

$final_message = $final_message.join('')
puts $final_message
