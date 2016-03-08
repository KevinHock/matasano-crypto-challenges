require "openssl"
require "base64"

File.readlines('gistfile1.txt').each do |line|
	i = 0

	# Split into array of 16-char arrays and see if any of them match every other 
	decoded_line = Base64.decode64(line)
	matasanoIntern2014 = decoded_line.scan(/.{16}/)
	matasanoIntern2014.each_with_index do |element,index|
  		for element in matasanoIntern2014 do
		  if matasanoIntern2014[index] == element
		  	i=i+1
		  end
		end
	end

	if i>20
		puts "The line is #{line}"
	end
end