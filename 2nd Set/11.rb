require "SecureRandom"

# quote = "Jesus Christ, Marty. If that's what you think, I'm disappointed in you. There never was an Aaron, counselor. [winks] Come on, I thought you had it figured there at the end. The way you put me on the stand like that, that was brilliant. The whole \"act-like-a-man\" thing. I knew exactly what you wanted. It was like we were dancing, Marty! Don't be like that, Marty. We did it, man! We fucking did it! We're a great team, you and me. You think I could've done this without you? [Martin continues walking out] You're feeling angry because you started to care about old Aaron, but... love hurts, Marty! What can I say? I'm just kidding, bud! I didn't mean to hurt your feelings! What else was I supposed to do?! You'll thank me down the road, 'cause this'll toughen you up, Martin Vail! You hear me? That's a promise!"
quote = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"

rytes = SecureRandom.random_bytes(16)

# to ecb or not ecb
zeroIfECB = rand(2)

# number of rytes before
beforeCount = rand(6)
beforeCount += 5

# number of rytes after
afterCount = rand(6)
afterCount += 5

beforeRytes = SecureRandom.random_bytes(beforeCount)
afterRytes = SecureRandom.random_bytes(afterCount)

input = beforeRytes + quote + afterRytes

#if and else for ecb vs cbc
if zeroIfECB == 0
	puts "ECB"
	cipher = OpenSSL::Cipher::AES.new(128, :ECB)
	cipher.encrypt
	cipher.key = rytes
	result = cipher.update(input) + cipher.final
else
	puts "CBC"
	cipher = OpenSSL::Cipher::AES.new(128, :CBC)
	cipher.encrypt
	cipher.key = rytes
	iv = cipher.random_iv
	result = cipher.update(input) + cipher.final
end

# DETECT ECB OR CBC BY USING #8 MOSTLY
i=0
crypted_blocks = result.scan(/.{16}/)
puts "The number of crypted_blocks is #{crypted_blocks.length}"
puts crypted_blocks[3]
crypted_blocks.each_with_index do |element,index|
  		for element in crypted_blocks do
		  if crypted_blocks[index] == element
		  	i=i+1
		  end
		end
	end

# Not totally accurate but idk why the number of crypted_blocks becomes 2 or 3 sometimes
if i == crypted_blocks.length
	puts "CBC"
else
	puts "ECB"
end