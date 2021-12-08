

class Day7:
    def __init__(self):
        self.parseData()
        self.part1()
        self.part2()
    
    def parseData(self):
        with open("input.txt","r") as file:
            data = file.read()
        self.positions = list(map(int,data.split(",")))
    
    def part1(self):
        positionFuel = {}

        for endPosition in range(1,max(self.positions)+1):
            fuel = 0
            for crabPosition in self.positions:
                fuel += abs(endPosition - crabPosition)
            positionFuel[endPosition] = fuel

        result = self.getBestPosition(positionFuel)
        print(f"Best Position is {result['best']} which uses {result['fuel']} fuel")

    def part2(self):
        positionFuel = {}

        for endPosition in range(1,max(self.positions)+1):
            fuel = 0
            for crabPosition in self.positions:
                posDelta = abs(endPosition - crabPosition)
                fuel += (posDelta**2 + posDelta) /2
            positionFuel[endPosition] = fuel

        result = self.getBestPosition(positionFuel)
        print(f"Best Position is {result['best']} which uses {result['fuel']} fuel")
    
    def getBestPosition(self,positionDict):
        # Sort by least fuel
        positionDict = dict(sorted(positionDict.items(), key=lambda item: item[1]))
        bestPosition = list(positionDict.items())[0][0]

        return {"best": bestPosition, "fuel": positionDict[bestPosition]}

if __name__ == "__main__":
    Day7()