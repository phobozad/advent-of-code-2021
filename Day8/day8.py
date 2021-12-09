

class Day8:
    def __init__(self):
        self.parseData()
        self.part1()
        self.part2()
    
    def parseData(self):
        with open("input.txt","r") as file:
            data = file.read()

        self.dataList = []

        for line in data.splitlines():
            entry = line.split("|")
            patterns = entry[0].split()
            digits = entry[1].split()
            self.dataList.append({"patterns": patterns, "digits": digits})
    
    def part1(self):
        digitCount = {}
        for i in range(10):
            digitCount[i] = 0

        for entry in self.dataList:
            for digit in entry['patterns']:
                # 1
                if len(digit) == 2:
                    digitCount[1] += 1
                # 4
                if len(digit) == 4:
                    digitCount[4] += 1
                # 7
                if len(digit) == 3:
                    digitCount[7] += 1
                # 8
                if len(digit) == 7:
                    digitCount[8] += 1
        
        sum = 0
        for digit,count in digitCount.items():
            sum += count

        print(f"Total Easy Digits: {sum}")

    def part2(self):
        
        outputValues = []
        # Decode the segment mapping
        for entry in self.dataList:
            
            digitMapping = {}
            for i in range(10):
                digitMapping[i] = ""

            for digitString in entry['patterns']:
                strLength = len(digitString)
                # 1
                if strLength == 2:
                    digitMapping[1] = [ letter for letter in digitString ]
                    
                # 4
                if strLength == 4:
                    digitMapping[4] = [ letter for letter in digitString ]
                # 7
                if strLength == 3:
                    digitMapping[7] = [ letter for letter in digitString ]
                # 8
                if strLength == 7:
                    digitMapping[8] = [ letter for letter in digitString ]
            
            # 3
            for digitString in entry['patterns']:
                # Both right segments = 9/3/0
                # If we have both right segments and total segments = 5, then its 3
                if len(digitString) == 5 and all(letter in digitString for letter in digitMapping[1]):
                    digitMapping[3] = [ letter for letter in digitString ]
                    break
            
            # 0/6/9 - 6 segments
            for digitString in entry['patterns']:
                # If it has 6 segments and it matches all of 3's segments, its a 9
                if len(digitString) == 6 and all(letter in digitString for letter in digitMapping[3]):
                    digitMapping[9] = [ letter for letter in digitString ]
                # Otherwise if it matches all of 1's segments, its a zero
                elif len(digitString) == 6 and all(letter in digitString for letter in digitMapping[1]):
                    digitMapping[0] = [ letter for letter in digitString ]
                # Otherwise its a 6
                elif len(digitString) == 6:
                    digitMapping[6] = [ letter for letter in digitString ]
            
            # 2/5 - 5 segments
            # Compare 8 vs 6.  The difference is has the top-right segment.
            # That top-right segment letter will be in 2 but not 5
            topRightSeg = set(digitMapping[8]) - set(digitMapping[6])

            for digitString in entry['patterns']:
                # Ignore 3's
                if len(digitString) == 5:
                    if not all(letter in digitString for letter in digitMapping[3]):
                        # Top-right segment present means its a 2
                        if all(letter in digitString for letter in topRightSeg):
                            digitMapping[2] = [ letter for letter in digitString ]
                        else:
                            digitMapping[5] = [ letter for letter in digitString ]

            digits=[]
            for digitString in entry['digits']:
                for digit,letterMap in digitMapping.items():
                    if all(letter in digitString for letter in letterMap) and len(digitString) == len(letterMap):
                        # Matching number, add it to the list
                        digits.append(digit)
                        break
            
            outputValues.append(int(''.join(map(str,digits))))
        
        print(f"Output Sum: {sum(outputValues)}")

if __name__ == "__main__":
    Day8()