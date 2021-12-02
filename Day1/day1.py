

with open("day1-input.txt","r") as file:
    data = file.read().splitlines()

# Cast data to int
data = map(int,data)
increaseCount = 0

for index, depth in enumerate(data,start = 0):

    # Skip first measurement
    if index != 0:
        if depth > lastDepth:
            increaseCount+=1
    
    lastDepth = depth


print(f"Depth increased {increaseCount} times")
