from math import prod

class Day9:
    def __init__(self):
        self.parseData()
        
        # Initalize 2d list for tracking which points we already counted
        self.pointsChecked = [ [False] * len(self.heightMap[0]) for x in range(len(self.heightMap)) ]

        self.part1()
        self.part2()
    
    def parseData(self):
        with open("input.txt","r") as file:
            data = file.read()

        self.heightMap = []

        for row in data.splitlines():
            self.heightMap.append(list(map(int,[ column for column in row ])))
        
    def part1(self):
        
        self.lowPoints = []
        for row, rowData in enumerate(self.heightMap):
            for column, dataPoint in enumerate(rowData):

                lowerWest = True
                lowerEast = True
                lowerNorth = True
                lowerSouth = True

                edges = self.checkEdge((row,column))

                if not edges['west']:
                    lowerWest = self.heightMap[row][column-1] > dataPoint
                if not edges['east']:
                    lowerEast = self.heightMap[row][column+1] > dataPoint
                if not edges['north']:
                    lowerNorth = self.heightMap[row-1][column] > dataPoint
                if not edges['south']:
                    lowerSouth = self.heightMap[row+1][column] > dataPoint

                if lowerWest and lowerEast and lowerNorth and lowerSouth:
                    # We are at a low point, record it in the list as a tuple
                    self.lowPoints.append((row,column))

        riskSum = 0
        for point in self.lowPoints:
            riskSum += 1 + self.heightMap[point[0]][point[1]]
        
        print(f"Risk Level Sum: {riskSum}")

    def part2(self):
        basins = []
        for point in self.lowPoints:
            basins.append(self.getHigherPointCountAll(point)+1)
        basinProd = prod(sorted(basins,reverse=True)[:3])
        print(f"Largest basins value: {basinProd}")
    
    def checkEdge(self, point):
        edge = {"north": False, "south": False, "east": False, "west": False}

        # Check west (first column)
        if point[1] == 0:
            edge['west'] = True
        # Check east (last column)
        if point[1] == len(self.heightMap[point[0]]) - 1:
            edge['east'] = True
        # Check north (first row)
        if point[0] == 0:
            edge['north'] = True
        # Check south (last row)
        if point[0] == len(self.heightMap) - 1:
            edge['south'] = True

        return edge
    
    def getHigherPointCountAll(self, point):
        higherPointCountSum = 0

        for direction in ["north", "south", "east", "west"]:
            higherPointCountSum += self.getHigherPointCount(point,direction)
        
        return higherPointCountSum

    def getHigherPointCount(self, point, direction):
        directionVector = {"north": -1, "south": 1, "west": -1, "east": 1}
        higherPointCount = 0
        
        lastHeight = self.heightMap[point[0]][point[1]]
        if direction in ["north", "south"]:
            # Max distance is bounded by the size of our heightmap
            distanceToEdge = point[0] if direction == "north" else len(self.heightMap)-1 - point[0]
            for i in range(distanceToEdge):
                # As long as we're higher than the last point, we're still in the basin
                curPoint = (point[0] + (i+1)*directionVector[direction], point[1])
                curHeight = self.heightMap[curPoint[0]][curPoint[1]]
                if curHeight > lastHeight and curHeight != 9:
                    # Only add to our count if we didn't already count this point
                    if not self.pointsChecked[curPoint[0]][curPoint[1]]:
                        higherPointCount += 1
                        self.pointsChecked[curPoint[0]][curPoint[1]] = True
                    lastHeight = curHeight
                    # Recurse for each point we look at to get the whole space
                    higherPointCount += self.getHigherPointCountAll(curPoint)
                else:
                    # If we aren't higher than the last point we're no longer in the basin
                    break
        else:
            # Max distance is bounded by the size of our heightmap
            distanceToEdge = point[1] if direction == "west" else len(self.heightMap[point[0]])-1 - point[1]
            for i in range(distanceToEdge):
                # As long as we're higher than the last point, we're still in the basin
                curPoint = (point[0], point[1] + (i+1)*directionVector[direction])
                curHeight = self.heightMap[curPoint[0]][curPoint[1]]
                if curHeight > lastHeight and curHeight != 9:
                    # Only add to our count if we didn't already count this point
                    if not self.pointsChecked[curPoint[0]][curPoint[1]]:
                        higherPointCount += 1
                        self.pointsChecked[curPoint[0]][curPoint[1]] = True
                    lastHeight = curHeight
                    # Recurse for each point we look at to get the whole space
                    higherPointCount += self.getHigherPointCountAll(curPoint)
                else:
                    # If we aren't higher than the last point we're no longer in the basin
                    break
        
        return higherPointCount

if __name__ == "__main__":
    Day9()