

with open("day2-input.txt","r") as file:
    data = file.read().splitlines()


horizontal = 0
depth = 0

for command in data:

    cmdArray = command.split()
    cmdAction = cmdArray[0]
    cmdValue = int(cmdArray[1])

    # directionVector will either be 1 or -1 depending on how the value should be adjusted
    if "up" in cmdAction:
        # "up" decreases depth, so use -1 for our vector
        directionVector = -1
    else:
        # Everything else adds to the current value
        directionVector = 1

    if "up" in cmdAction or "down" in cmdAction:
        # up/down affects depth
        depth = depth + cmdValue*directionVector
    else:
        # only other command option is "forward", which affects horizontal position
        horizontal = horizontal + cmdValue*directionVector


print(f"Horizontal: {horizontal} | Depth: {depth} | MultipliedValue: {horizontal*depth}")
