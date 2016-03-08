require "openssl"
require "base64"

# POTENTIAL PROBLEMS
# I didn't pad and assumed input was always divisible by 16?
# 

# // ------------------------------------------------------------

# 10. Implement CBC Mode

# In CBC mode, each ciphertext block is added to the next plaintext
# block before the next call to the cipher core.

# The first plaintext block, which has no associated previous ciphertext
# block, is added to a "fake 0th ciphertext block" called the IV.

# Implement CBC mode by hand by taking the ECB function you just wrote,
# making it encrypt instead of decrypt (verify this by decrypting
# whatever you encrypt to test), and using your XOR function from
# previous exercise.

# DO NOT CHEAT AND USE OPENSSL TO DO CBC MODE, EVEN TO VERIFY YOUR
# RESULTS. What's the point of even doing this stuff if you aren't going
# to learn from it?

# The buffer at:

#     https://gist.github.com/3132976

# is intelligible (somewhat) when CBC decrypted against "YELLOW
# SUBMARINE" with an IV of all ASCII 0 (\x00\x00\x00 &c)

# // ------------------------------------------------------------

#
#
# set plain
plain = "YELL0W SUBMARINEYELL1W SUBMARINEYELL2W SUBMARINEYELL3W SUBMARINEYELL4W SUBMARINE"

# 
# split up plaintext in 16 byte blocks
plain_blocks = plain.scan(/.{16}/)

#
# initiate xor with
xorWith = String.new("\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")

#
#
final_array = Array.new()

# 
# Loop
 for i in 0..plain_blocks.length-1
	#
	# ecbinput = plaintext xor'd w/ xorWith
	ecbinput = plain_blocks[i].unpack('C*').zip(xorWith.unpack('C*')).map{ |plain_blocks[i],xorWith| plain_blocks[i] ^ xorWith }.pack('C*')
	# 
	# ecb
	cipher = OpenSSL::Cipher::AES.new(128, :ECB)
	cipher.padding = 0
	cipher.encrypt
	cipher.key = "YELLOW SUBMARINE"
	matasano_intern_2014 = cipher.update(ecbinput) + cipher.final
	# 
	# add output to final output
	final_array << matasano_intern_2014
	# 
	# xorWith = output
	xorWith = matasano_intern_2014
end

final_result = final_array.join("")

puts final_result