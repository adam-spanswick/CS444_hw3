# CS444 Homework 3, Problem 2, Crypto Challenge 6
#
# Adam Spanswick
#
# Source for diving string int n parts: http://code.activestate.com/recipes/496784-split-string-into-n-size-pieces/
# Source for character frequencies: https://en.wikipedia.org/wiki/Letter_frequency

import base64 
import codecs

file_to_decrypt = open("6.txt", "rb")
base64_file = base64.b64decode(file_to_decrypt.read())
key_sizes = [i for i in range(2,41)]

# Scores text by using character frequencies found on wikipedia
# Source: https://en.wikipedia.org/wiki/Letter_frequency
# For the space character I guessed the value
def scoreText(msg):
	char_freqs = {'a': .08167, 'b': .01492, 'c': .02782, 'd': .04253, 'e': .12702,
	'f': .02228, 'g': .02015, 'h': .06094, 'i': .06966, 'j': .001532, 'k': .0772, 'l': .04025,
	'm': .02406, 'n': .06749, 'o':.07507, 'p': .01929, 'q': .0095, 'r': .05987, 's': .06327,
	't': .09056, 'u': .02758, 'v': .00978, 'w': .0236, 'x': .00150, 'y': .01974, 'z': .0074, ' ': .15}

	score = 0
	for c in msg: 
		if c in char_freqs:
			score  = score + char_freqs.get(c)
	
	return score

# Computes a single character XOR by looping over all characters, XORing them
# with the encoded message, and then using character frequency to score the xored
# message. The maximum score is the most likely to be plain text.
def Single_Char_XOR(str_to_decode):
	single_char = [chr(i) for i in range(0, 255)]
	msg_score_lst = []
	msg_char_lst = []

	for i in single_char:
		msg = ""
		for j in str_to_decode:
			x = j ^ ord(i)
			x = chr(x)
			msg += x
		msg_score = scoreText(msg)
		msg_score_lst.append((msg, msg_score))
		msg_char_lst.append((msg, i))

	max_score = 0
	max_score_msg = ""
	for i in msg_score_lst:
		if i[1] > max_score:
			max_score = i[1]
			max_score_msg = i[0]

	max_score_char = ''
	for i in msg_char_lst:
		if i[0] == max_score_msg:
			max_score_char = i[1]
	result = ord(max_score_char)
	return result

# Compute hamming distance by XORing the two inputs and counting the 1's
# in the result which are the difference in the inputs
def Compute_Dist(str1, str2):
	distance = 0.0
	str1_bytes = bytearray(str1)
	str1_bin = []
	str2_bytes = bytearray(str2)
	str2_bin = []

	xored_bytes = []
	for b1 in range(len(str1_bytes)):
		xor = str1_bytes[b1] ^ str2_bytes[b1]
		xored_bytes.append(xor)

	binary = ""
	for i in range(len(xored_bytes)):
		b = bin(xored_bytes[i])[2:]
		binary += str(b)

	for i in binary:
		if i == '1':
			distance = distance + 1
	return distance

#Loop over all the keysizes and compute the hamming distances for each 
norm_dists = {}
for key_size in key_sizes:
	# Break ciphertext into key size blocks
	text_in_keysize_chunks = [base64_file[j:j+key_size] for j in range(0, len(base64_file),key_size)]

	# Take 4 key sized blocks instead of 2
	blocks = []
	dist_key_size = []
	for j in range(4):
		block = text_in_keysize_chunks[j]
		blocks.append(block)

	key_block1 = blocks[0]
	key_block2 = blocks[1]
	key_block3 = blocks[2]
	key_block4 = blocks[3]

	# Compute the distance between each pair of blocks
	dist1 = Compute_Dist(key_block1, key_block2)
	dist2 = Compute_Dist(key_block1, key_block3)
	dist3 = Compute_Dist(key_block1, key_block4)
	dist4 = Compute_Dist(key_block2, key_block3)
	dist5 = Compute_Dist(key_block2, key_block4)
	dist6 = Compute_Dist(key_block3, key_block4)
	dist_key_size.append(dist1)
	dist_key_size.append(dist2)
	dist_key_size.append(dist3)
	dist_key_size.append(dist4)
	dist_key_size.append(dist5)
	dist_key_size.append(dist6)

	# Now, average the distances and divide by the total distances
	avg_sum_dists = sum(dist_key_size)/6
	# Normalize the distances by dividing by key size
	norm_dist = avg_sum_dists/key_size
	norm_dists[key_size] = norm_dist

keys = norm_dists.keys()
distances = norm_dists.values()

# Compute the min distance 
min_distance = min(distances)
possible_key_size = 0
for i,j in norm_dists.items():
	if j == min_distance:
		possible_key_size = i
# Uncomment to see best key size
# print("Key Size: " + str(possible_key_size)) 

# Loop over the best key size and transpose the blocks by 1st byte, 2nd byte etc.. through length key size
transposed_blocks = []
for i in range(possible_key_size):
	single_char_block = bytearray()
	for j in range(i, len(base64_file), possible_key_size):
		single_char_block.append(base64_file[j])
	transposed_blocks.append(single_char_block)

# Loop over transposed blocks and pass each to single char xor function to build up the key
key = bytearray()
for tblock in transposed_blocks:
	single_char_decoded = Single_Char_XOR(tblock)
	key.append(single_char_decoded)

# Uncomment to see key
# print(key) 

# Decode with repeating key xor
# Loop over the encoded text and XOR each byte of the key with a byte from the file
# Repeat the key when key_idx = key length
key_idx = 0
decoded_txt = []
for i in range(len(base64_file)):
	txt = key[key_idx] ^ base64_file[i]
	# Reset the key index to the beginning of the key after we loop through key size
	# indices in the cipher text 
	if (key_idx+1) % possible_key_size == 0:
		key_idx = 0
	else: 
		key_idx = key_idx + 1
	decoded_txt.append(txt)

decoded = ""
for i in decoded_txt:
	i = chr(i)
	decoded += i
print(decoded)





