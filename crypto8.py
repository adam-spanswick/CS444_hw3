# CS444 Homework 3, Problem 2, Crypto Challenge 8
#
# Adam Spanswick

file = open("8.txt", "r")
groups = 16

# Read in the lines from the encrypted text 
blocks = []
while True:
	cipher_text = file.readline()
	blocks.append(cipher_text)
	if not cipher_text:
		break

# Since we know the block size is 16, break each cipher text into 16 byte chunks
block_sizes = []
for block in blocks:
	block = [block[j:j+groups] for j in range(0, len(block), groups)]
	block_sizes.append(block)

# Counts repeating blocks from the encrypted text. In ECB a block of plain text always produces the same cipher text.
# So we count the repeating blocks and take the max, which will be the most likely to be encrypted with AES in ECB.
repetitions = {}
line_num = 1
for block in block_sizes:
	reps = 0
	for b in block:
		for b2 in block:
			if b == b2:
				reps = reps + 1
	repetitions[line_num] = reps
	line_num = line_num + 1

# Take the maximum number of repeated blocks. It should be the block encrypted with AES in ECB.
max_repeats = max(repetitions.values())

max_repear_line_num = 0
for i,j in repetitions.items():
	if j == max_repeats:
		max_repear_line_num = i

print("Line Number: " + str(max_repear_line_num) + ", Repeated Cipher Blocks: " + str(max_repeats))
		



