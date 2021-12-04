from bitarray import bitarray
from bitarray.util import ba2int

with open("day3-input.txt","r") as file:
    data = file.read().splitlines()

# Map input data to bitarrays
data = list(map(bitarray,data))
datawidth = len(data[0])

# rating[0] = CO2; rating[1] = Oxygen
rating = []
for rateParam in range(2):
    filteredData = data
    for bitPos in range(datawidth):
        bitcount = 0
        for bits in filteredData:
            if bits[bitPos]:
                bitcount+=1
        if bitcount >= len(filteredData)/2:
                criteria = 0 + rateParam
        else:
                criteria = 1 - rateParam
        
        filteredData = [bits for bits in filteredData if bits[bitPos] == criteria]
        # Stop if we are down to one datapoint
        if len(filteredData) == 1:
            break

    rating.append(filteredData[0])


print(f"CO2: {ba2int(rating[0])}  |  Oxygen: {ba2int(rating[1])}  |  Answer: {ba2int(rating[0]) * ba2int(rating[1])}")




