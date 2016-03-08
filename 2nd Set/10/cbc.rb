require "openssl"

data = "YELLOW SUBMARINE"
fuck = "YELLOW SUBMARINE"

# puts data.length
puts "Right answer is "
puts "-------------------------------------"
decipher = OpenSSL::Cipher::AES.new(128, :CBC)
decipher.encrypt
decipher.key = "YELLOW SUBMARINE"

right_answer = decipher.update("YELLOW SUBMARINE") + decipher.final
puts right_answer
puts "-------------------------------------"

# plainblocks = data.scan(/.{16}/)
# puts plainblocks
# blocks_cbc = Array.new

# replace = plainblocks[1]

# blocks_cbc.push(plainblocks[0])
# blocks_cbc.push(plainblocks[0].unpack('C*').zip(plainblocks[1].unpack('C*')).map{ |plainblocks[0],plainblocks[1]| plainblocks[0] ^ plainblocks[1] }.pack('C*'))
# blocks_cbc.push(replace.unpack('C*').zip(plainblocks[2].unpack('C*')).map{ |replace,plainblocks[2]| replace ^ plainblocks[2] }.pack('C*'))

# combined = plainblocks.join("")

# puts combined

puts "My answer is "
puts "-------------------------------------"
obert = OpenSSL::Cipher::AES.new(128, :ECB)
obert.encrypt
obert.key = "YELLOW SUBMARINE"



my_answer = obert.update("YELLOW SUBMARINE".delete("\000")) + obert.final
puts my_answer.length
puts "-------------------------------------"
# puts my_answer.length
# puts right_answer[1].to_i
