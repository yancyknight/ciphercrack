from __future__ import division
from Crypto.Cipher import AES # pip install pycrypto

# READ FILES
cipherfile = open('ciphertext.txt', 'r')
ciphertext = cipherfile.read()

plainfile = open('plaintext.txt', 'r')
plaintext = plainfile.read()

dictionaryfile = open('dictionary.txt', 'r')
words = dictionaryfile.read()
words = words.split('\n')

# SET IV
iv = '00000000000000000000000000000000'
iv = bytearray.fromhex(iv)
iv = str(iv)

# LOOP THROUGH POSSIBLE PASSWORDS
for i, passwd in enumerate(words):
    if len(passwd) > 16:
        continue
    padded_pass = passwd.strip().ljust(16)

    # SET UP ENCRYPTION SUITE
    pass_enc = AES.new(padded_pass, AES.MODE_CBC, iv)

    # PAD PLAINTEXT WITH PKCS5
    length = 16 - (len(plaintext) % 16)
    padded_plaintext = plaintext + chr(length) * length

    # ENCRYPT PLAINTEXT
    encrypted_text = pass_enc.encrypt(padded_plaintext)
    encrypted_text = "".join("{:02x}".format(ord(c)) for c in encrypted_text)

    # CHECK IF THEY MATCH
    if encrypted_text == ciphertext:
        print 'Password found in', i + 1, 'tries'
        print 'Password:', passwd
        exit()

print 'No matches found,', len(words), 'passwords attempted'