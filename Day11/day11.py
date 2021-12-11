

class Day11:
    def __init__(self):       
        self.part1()
        self.part2()
    
    def parseData(self):
        with open("input.txt","r") as file:
            data = file.read()

        self.energyGrid = []
 
        for row in data.splitlines():
            rowData = list(map(int,[ column for column in row ]))
            # Tip from Day 9 participants - pad the grid with special value to ease edge checks
            rowData.insert(0,"#")
            rowData.append("#")
            self.energyGrid.append(rowData)
    
        # Top row padding
        self.energyGrid.insert(0,["#"]*len(self.energyGrid[0]))
        # Bottom row padding
        self.energyGrid.append(["#"]*len(self.energyGrid[0]))
        
    def part1(self):
        self.parseData()
        self.flashCount = 0

        for step in range(100):
            # Use cardinal numbering for us human plebs
            step = step + 1
            self.flashList = []

            for row,rowData in enumerate(self.energyGrid):
                for column in range(len(rowData)):
                    self.increaseEnergy(row,column)

            # Any ocotpus that flashed has energy level reset to 0
            for row,column in self.flashList:
                self.energyGrid[row][column] = 0

        print(f"There were a total of {self.flashCount} flashes")

    def part2(self):
        self.parseData()
        self.flashCount = 0

        # Loop until our flash list includes every octopus
        # Account for padding on each side 2 vertical, 2 horizontal
        numOctopus = (len(self.energyGrid[0]) - 2) * (len(self.energyGrid) - 2)
        step = 0
        while len(self.flashList) != numOctopus:
            step += 1
            self.flashList = []

            for row,rowData in enumerate(self.energyGrid):
                for column in range(len(rowData)):
                    self.increaseEnergy(row,column)

            # Any ocotpus that flashed has energy level reset to 0
            for row,column in self.flashList:
                self.energyGrid[row][column] = 0

        print(f"First simultaneous flash at step: {step}")

    def flashOcto(self,row,column):
        # Only flash once per step
        if (row,column) in self.flashList:
            return

        # Mark this octopus as flashed
        self.flashList.append((row,column))
        self.flashCount += 1

        # Increase adjacent energy levels, checking if each of those might flash
        
        # Check to the left/right
        for adjustColumn in [-1,1]:
            for adjustRow in range(-1,2):
                curRow = row + adjustRow 
                curCol = column + adjustColumn
                self.increaseEnergy(curRow,curCol)
            
        # Check top/bottom
        for adjustRow in [-1,1]:
            curRow = row + adjustRow
            self.increaseEnergy(curRow,column)
            
    def increaseEnergy(self,row,column):
        # Ignore padding
        if self.energyGrid[row][column] == "#":
            return
        
        self.energyGrid[row][column] += 1
        if self.energyGrid[row][column] > 9:
            self.flashOcto(row,column)


if __name__ == "__main__":
    Day11()