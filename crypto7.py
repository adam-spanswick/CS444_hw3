# CS444 Homework 3, Problem 2, Crypto Challenge 7
#
# Adam Spanswick
#
# Sources: https://pycryptodome.readthedocs.io/en/latest/src/cipher/aes.html

import base64
from Crypto.Cipher import AES

# Decrypts the text using AES from Crypto.Cipher 
def Decrypt_AES_ECB(encrypted_text, key):
	encrypted_text = base64.b64decode(encrypted_text)

	decrypted = AES.new(key, AES.MODE_ECB)
	text = decrypted.decrypt(encrypted_text)

	return text

file_to_decrypt = open("7.txt", "r+")
key = "YELLOW SUBMARINE"

encrypted_text = file_to_decrypt.read()

decrypted_text = Decrypt_AES_ECB(encrypted_text, key)
print(decrypted_text)