require "openssl"
require "base64"

idk = File.read('gistfile1.txt')

encrypted = Base64.decode64(idk)

puts encrypted

decipher = OpenSSL::Cipher::AES.new(128, :CBC)
decipher.decrypt
decipher.key = "YELLOW SUBMARINE"

plain = decipher.update(encrypted) + decipher.final

puts plain