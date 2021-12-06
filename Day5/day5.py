import numpy as np

class day5:
    def __init__(self):
        self.parseData()
        self.part1()
        self.part2()
    
    def parseData(self):
        with open("day5-input.txt","r") as file:
            data = file.read().splitlines()
       
        # Note - Numpy uses inverse coordinates (y,x) not (x,y)

        # Track horizontal/vertical (straight) lines separate from diagonal for part1/part2
        lineSegments = { "straight": [], "diagonal": [] }
        xMax = 0
        yMax = 0
        for line in data:
            x1, y1, x2, y2 = list(map(int,line.replace(" -> ",",").split(",")))
            
            # horizontal/vertical lines only have changes in x or y but not both
            if x1!=x2 and y1!=y2:
                lineType = "diagonal"
            else:
                lineType = "straight"

            points=[]
            done = False
            while not done:
                points.append((x1,y1))

                # Need to check if we are now at the final point and exit the loop if so
                if x1==x2 and y1==y2:
                    done = True

                if x1<x2:
                    x1 += 1
                elif x1>x2:
                    x1 += -1

                if y1<y2:
                    y1 += 1
                elif y1>y2:
                    y1 += -1
            
            lineSegments[lineType].append(points)
            xMaxSegment = max(points,key=lambda item:item[0])[0] + 1
            yMaxSegment = max(points,key=lambda item:item[1])[1] + 1

            # Keep track of the largest line in the whole dataset to size the numpy matrix appropriately
            if xMaxSegment > xMax:
                xMax = xMaxSegment
            if yMaxSegment > yMax:
                yMax = yMaxSegment

        # Create dict of lists of line matrices = one matrix per line segment
        self.lineMatrix = {}
        for lineType, lines in lineSegments.items():
            self.lineMatrix[lineType] = []

            for line in lines:
                # Create matrix sized based on the largest x and y values
                matrix = np.zeros((yMax,xMax),dtype=np.uint16)
                
                # Mark each point in the matrix with a 1
                for point in line:
                    matrix[point[1],point[0]] = 1 
                
                self.lineMatrix[lineType].append(matrix)

    def part1(self):
        # Add all the individual line matrices together to get the full map
        ventMap = sum(self.lineMatrix["straight"])
        
        # Find all points where two or more lines overlap
        overlapCount = np.count_nonzero(ventMap >= 2)

        print(f"Sraight Line Only Overlap Points: {overlapCount}")
         
    def part2(self):
        # Add all the individual line matrices together to get the full map
        ventMap = sum(self.lineMatrix["straight"] + self.lineMatrix["diagonal"])
        
        # Find all points where two or more lines overlap
        overlapCount = np.count_nonzero(ventMap >= 2)

        print(f"All Overlap Points: {overlapCount}")
        pass

if __name__ == "__main__":
    day5()
