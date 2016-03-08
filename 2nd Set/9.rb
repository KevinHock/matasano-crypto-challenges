# 9. Implement PKCS#7 padding

# Pad any block to a specific block length, by appending the number of
# bytes of padding to the end of the block. For instance,

#   "YELLOW SUBMARINE"

# padded to 20 bytes would be:

#   "YELLOW SUBMARINE\x04\x04\x04\x04"

# The particulars of this algorithm are easy to find online.

puts 'Hello there, can you tell me the block size?'
block_size = gets.to_i

puts 'Can you now tell me the string?'
string = gets

# Mod the size of the string by the block size
puts block_size
puts string.length
padding = block_size-string.length

puts padding

# Save value in decimal to not confuse the crap out of myself
matasano_intern_2014 = padding

# Turn value into hex
padding = padding.to_s(16)

# Get rid of \n
string = string.chomp

if matasano_intern_2014 != 0
	for i in 1 .. matasano_intern_2014
		
		# Cat the string with padding
		if matasano_intern_2014 < 16
			string = string + "0"
		end

		puts "Adding #{i} " + padding.to_s

		string = string + padding.to_s
	end
end

puts "With PKCS#7 padding your string is " + '"' + string + '"' 
