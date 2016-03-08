# 7. AES in ECB Mode

# The Base64-encoded content at the following location:

#     https://gist.github.com/3132853

# Has been encrypted via AES-128 in ECB mode under the key

#     "YELLOW SUBMARINE".

# (I like "YELLOW SUBMARINE" because it's exactly 16 bytes long).

# Decrypt it.

# Easiest way:

# Use OpenSSL::Cipher and give it AES-128-ECB as the cipher.

# What's in the box?

require 'openssl'
require "base64"

contents = File.read('gistfile1.txt')
notSixFour = Base64.decode64(contents)
matasanoInternChicagoSummer2014 = OpenSSL::Cipher::AES.new(128, :ECB)
matasanoInternChicagoSummer2014.decrypt
matasanoInternChicagoSummer2014.key = "YELLOW SUBMARINE"
done = matasanoInternChicagoSummer2014.update(notSixFour) + matasanoInternChicagoSummer2014.final
print done