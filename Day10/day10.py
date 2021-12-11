

class Day10:
    def __init__(self):
        self.errorScoreMap = {")": 3, "]": 57, "}": 1197, ">": 25137}
        self.autocompleteScoreMap = {"(": 1, "[": 2, "{": 3, "<": 4}
        self.openingTokenMap = {")": "(", "]": "[", "}": "{", ">": "<"}
        self.parseData()
        
        self.part1()
        self.part2()
    
    def parseData(self):
        with open("input.txt","r") as file:
            self.data = file.read().splitlines()
        
    def part1(self):
        errorScore = 0
        self.incompleteLines = []

        for line in self.data:
            tokenList = []
            validLine = True
            for token in line:
                # Any opening tokens, append to the end of our token list tracker
                if token in self.openingTokenMap.values():
                    tokenList.append(token)
                elif token in self.openingTokenMap.keys():
                    # Any closing tokens, make sure the last opening token corresponds with this closing token
                    if tokenList[-1] == self.openingTokenMap[token]:
                        tokenList.pop()
                    else:
                        # Otherwise the line is corrupted
                        errorScore += self.errorScoreMap[token]
                        # Abandon further processing of this line
                        validLine = False
                        break
            # If the line wasn't corrupt, add it to the incompleteLines list
            if validLine:
                self.incompleteLines.append({"line": line, "tokens": tokenList})

        print(f"Total Syntax Error Score: {errorScore}")

    def part2(self):
        autocompleteScores = []
        for line in self.incompleteLines:
            autocompleteScore = 0
            for token in reversed(line['tokens']):
                autocompleteScore = autocompleteScore*5 + self.autocompleteScoreMap[token]
                
            autocompleteScores.append(autocompleteScore)
        
        autocompleteScores = sorted(autocompleteScores)
        # Get the middle value
        winningScore = autocompleteScores[int(len(autocompleteScores)/2)]
        print(f"Winning AutoComplete Score: {winningScore}")
    

if __name__ == "__main__":
    Day10()