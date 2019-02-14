import math
import os

# CS444 Homework 3, Problem 1
#
# Adam Spanswick

def Calc_Z_Score(bitString):
    runs_0 = 0
    runs_1 = 0
    total_runs = 0
    heads = 0
    tails = 0

    for i in range(len(bitString)):
        # Calculate the number of heads (1) and tails (0)
        if bitString[i] == "1":
            heads += 1
        elif bitString[i] == "0":
            tails += 1

        # Count the number of runs for heads and tails
        if bitString[i] == "1" and (i + 1) < len(bitString) and bitString[i] != bitString[i + 1]:
            runs_1 += 1
        elif bitString[i] == "0" and (i + 1) < len(bitString) and bitString[i] != bitString[i + 1]:
            runs_0 += 1

        # Make sure to count the last run in the data
        if i == (len(bitString) - 1) and bitString[i] == "0":
            runs_0 += 1
        elif i == (len(bitString) - 1) and bitString[i] == "1":
            runs_1 += 1

    total_runs = runs_0 + runs_1

    # Uncomment to print the number of runs for 1, 0 and the total number of runs
    # print(runs_1)
    # print(runs_0)
    # print(total_runs)

    # Calculate Z score
    E = ((2 * heads * tails) / (heads + tails)) + 1

    V = (2 * heads * tails * (2 * heads * tails - heads - tails)) / (pow((heads + tails), 2) * (heads + tails - 1))

    Z = (total_runs - E) / math.sqrt(V)

    # Uncomment to print the Z score
    # print(Z)

    # Determine if the data from dev/urandom is a good source of random or not
    # Print 1 if it is not a good source of random
    # Print 0 if it is a good source of random
    res = 2
    if Z > 1.96 or Z < -1.96:
        return 1
    else:
        return 0


rand = open("/dev/urandom", "rb")
class_file = open("class_bits.txt", "rb")
class_data = class_file.read().splitlines()

processed_class_data = []
for i in class_data:
    i = str(i)
    idx  = i.find(',')
    i =  i[idx+1:len(i)-1]
    processed_class_data.append(i)

urand_bytes = bytearray()
hex_bytes = []
binary = []

# Read in 512 bits from urandom
# Convert each byte to binary and store in an array
for i in range(64):
    byte = rand.read(1)
    byte = ord(byte)
    hex_byte = hex(byte)
    hex_bytes.append(hex_byte)
    binary.append(bin(byte))

# Remove the 0b from each binary byte
for i in range(len(binary)):
    b = binary[i][2:]
    binary[i] = b

# Create a binary string of the bits
b = ""
for i in range(len(binary)):
    b += binary[i]

urand_results = Calc_Z_Score(b)

class_Z_scores = []
for i in processed_class_data:
    class_results = Calc_Z_Score(i)
    class_Z_scores.append(class_results)

print("If the result is 0 then it is a good soure of randomness and 1 if it is not a good source of randomness:")
print("urandgood random (0), bad random (1): " + str(urand_results))
for i in range(len(class_data)):
    x = str(class_data[i])
    x = x[2:len(x)-1]
    res = x + ", good random (0), bad random (1): " + str(class_Z_scores[i])
    print(res)



