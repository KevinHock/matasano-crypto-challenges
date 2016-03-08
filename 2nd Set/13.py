# To exploit delete the last block and concat the 2nd
# 
# Sample:
	# Enter an email address: kevin@ghi.admin
	# user_prof is --------------------
	# email=kevin@ghi.admin&uid=1234567890123456&role=user
	# -------------------
	# length of user_prof is 52
	# email=kevin@ghi.admin&uid=1234567890123456&role=userAAAAAAAAAAAA
	# le2ngth of user_prof is 64
	# The encrypted profile is
	# a3:50:b2:7c:8e:b2:83:c3:d4:2b:24:11:6a:a2:ce:14:4e:22:d2:90:55:eb:5d:29:da:e6:03:da:93:dd:26:b6:05:ea:08:5a:1a:84:9e:95:40:6d:87:29:79:81:96:4d:df:17:11:48:88:da:94:c3:1d:7f:3a:4b:c7:aa:e6:db
	# Enter a ciphertext that will be decrypted: a3:50:b2:7c:8e:b2:83:c3:d4:2b:24:11:6a:a2:ce:14:4e:22:d2:90:55:eb:5d:29:da:e6:03:da:93:dd:26:b6:05:ea:08:5a:1a:84:9e:95:40:6d:87:29:79:81:96:4d:4e:22:d2:90:55:eb:5d:29:da:e6:03:da:93:dd:26:b6
	# email=kevin@ghi.admin&uid=1234567890123456&role=admin&uid=123456



# Write a k=v parsing routine, as if for a structured cookie. The
# routine should take:

#    foo=bar&baz=qux&zap=zazzle

# and produce:

#   {
#     foo: 'bar',
#     baz: 'qux',
#     zap: 'zazzle'
#   }

# (you know, the object; I don't care if you convert it to JSON).

import json

s="foo=bar&baz=qux&zap=zazzle"

cookie = dict(item.split("=") for item in s.split("&"))

print "cookie is ----------------"
print cookie
print "--------------------------------"



# Now write a function that encodes a user profile in that format, given
# an email address. You should have something like:

#   profile_for("foo@bar.com")

# and it should produce:

#   {
#     email: 'foo@bar.com',
#     uid: 10,
#     role: 'user'
#   }

# encoded as:

#   email=foo@bar.com&uid=10&role=user


# Your "profile_for" function should NOT allow encoding metacharacters
# (& and =). Eat them, quote them, whatever you want to do, but don't
# let people set their email address to "foo@bar.com&role=admin".

import re

g_uid = 1234567890123455

def profile_for(email):
    global g_uid
    g_uid += 1 #      'Eat them'
    return "email=" + re.sub('[&=]', '', email) + "&uid=" + str(g_uid) + "&role=user"

email = raw_input('Enter an email address: ')
user_prof = profile_for(email)
print "user_prof is --------------------"
print user_prof
print '-------------------'
print 'length of user_prof is '+str(len(user_prof))

for x in range(0, 16-len(user_prof)%16):
	user_prof += "A" # fake padding
print user_prof
print 'after padding length of user_prof is '+str(len(user_prof))


# now, two more easy functions. generate a random aes key, then:
import os
key = os.urandom(16) # yay urandom


#  (a) encrypt the encoded user profile under the key; "provide" that
#  to the "attacker".

from Crypto.Cipher import AES

obj = AES.new(key, AES.MODE_ECB)
ciphertext = obj.encrypt(user_prof)
print 'The encrypted profile is'
print ':'.join(x.encode('hex') for x in ciphertext)

chosen_ciphertext = raw_input('Enter a ciphertext that will be decrypted: ')
nocolons = re.sub('[:]', '', chosen_ciphertext)
normal = nocolons.decode("hex")

#  (b) decrypt the encoded user profile and parse it.
obj2 = AES.new(key, AES.MODE_ECB)
print obj2.decrypt(normal)
