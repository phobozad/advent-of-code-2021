

class Day6:
    def __init__(self):
        self.parseData()
        self.part1()
        self.part2()
    
    def parseData(self):
        with open("day6-input.txt","r") as file:
            data = file.read()

        self.fishStart = list(map(int,data.split(",")))
    
    def part1(self):
        #print(f"Fish after 80 days: {len(self.simulateFish(80,self.fishStart))}")
        print(f"Fish after 80 days: {self.simulateFishFast(80,self.fishStart)}")

    def part2(self):
        #print(f"Fish after 256 days: {len(self.simulateFish(256,self.fishStart))}")
        print(f"Fish after 256 days: {self.simulateFishFast(256,self.fishStart)}")

    def simulateFishFast(self,days,startingFish):       
        # Need to add extra days to the calendar for fish procreating on the last days so we don't IndexError
        procreationCalendar = [0]*(days+10)
        fishCount = len(startingFish)
        
        # Initial state value is 1 - their procreation day (ordinal vs cardinal)
        for fishValue in startingFish:
            procreationCalendar[fishValue+1] += 1
        
        for curDay in range(days+1):
            # Any fish that procreate on this day wil have offspring that
            # procreate 9 days from now
            procreationCalendar[curDay+9] += procreationCalendar[curDay]
            # They will also procreate themselves again in 7 days
            procreationCalendar[curDay+7] += procreationCalendar[curDay]
            # Add a fish to our population for every fish that procreated today
            fishCount += procreationCalendar[curDay]
        
        return fishCount

    # RIP memory/cpu for part 2 using original function
    def simulateFish(self,days,startingFish):
        # Make sure we create a new object copy so we don't modify it in place on subsequent simulations
        fishList = list(startingFish)
        
        for day in range(1,days+1):
            for fishNum, fishTimer in enumerate(fishList):
                fishList[fishNum] -= 1
                if fishTimer == 0:
                    fishList.append(9)
                    fishList[fishNum] = 6  
            
        return fishList

if __name__ == "__main__":
    Day6()