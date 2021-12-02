

with open("day1-input.txt","r") as file:
    data = file.read().splitlines()

# Cast data to int
data = list(map(int,data))
increaseCount = 0


windowSum = []
for window in range(0,int(len(data)/3)*3):
    windowSum.append(sum(data[window:window+3]))

for index, depth in enumerate(windowSum,start = 0):

    # Skip first measurement
    if index != 0:
        if depth > lastDepth:
            increaseCount+=1
    
    lastDepth = depth


print(f"Depth increased {increaseCount} times")
