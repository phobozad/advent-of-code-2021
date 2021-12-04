from bitarray import bitarray
from bitarray.util import ba2int

with open("day3-input.txt","r") as file:
    data = file.read().splitlines()

# Map input data to bitarrays
data = list(map(bitarray,data))
datawidth = len(data[0])
bitcount = [0] * datawidth

for index, bits in enumerate(data):
    for i in range(datawidth):
        if bits[i]:
            bitcount[i]+=1

gamma = bitarray(datawidth)
for i, bit in enumerate(bitcount):
    # Calculate gamma first
    if bit > len(data)/2:
        gamma[i] = 1
    else:
        gamma[i] = 0
    # Then epsilon is just the inverse of gamma
    epsilon = ~gamma

print(f"Gamma: {ba2int(gamma)}  |  Epsilon: {ba2int(epsilon)}  |  Answer: {ba2int(gamma) * ba2int(epsilon)}")