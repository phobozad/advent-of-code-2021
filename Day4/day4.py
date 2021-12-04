import numpy as np

class day4:
    def __init__(self):
        self.setupCards()
        self.part1()
        self.part2()
    
    def setupCards(self):
        with open("day4-input.txt","r") as file:
            data = file.read().splitlines()

        # Parse the bingo ball draws
        self.drawOrder = list(map(int,data[0].split(",")))

        self.bingoBoards = [[]]
        self.winningBoards = []
        curBoardIndex = 0

        for lineNum, line in enumerate(data):
            
            # Skip first two lines
            if lineNum in range (2):
                continue
            
            # Bingo card separators (blank lines) every 6 lines starting on line 1 (ordinal)
            if (lineNum - 1) % 6 == 0:
                # Add another bingo board
                curBoardIndex += 1
                self.bingoBoards.append([])
                # Skip and go to the next line
                continue
            
            # Otherwise parse the line and add it to the current Bingo card
            self.bingoBoards[curBoardIndex].append(list(map(int,line.split())))

        # Setup board marker matrix
        self.boardMarkers = [np.zeros((5,5)) for i in range(len(self.bingoBoards))]
    
    def part1(self):
        for bingoBall in self.drawOrder:
            # Mark all cards that have the drawn number
            self.markCards(bingoBall)
            
            # Check if anyone got Bingo
            winningCards = self.checkBingo()
            if winningCards is not False:

                # We might have more than one winner
                for cardID in winningCards:
                    # We score based on sum of unmarked (0) spaces
                    score = self.sumBoard(cardID,0) * bingoBall
                    print(f"BINGO on card: {cardID} with score: {score}")
                break
    
    def part2(self):
        for bingoBall in self.drawOrder:
            # Mark all cards that have the drawn number
            self.markCards(bingoBall)
            
            # Check if anyone got Bingo
            winningCards = self.checkBingo()
            if winningCards is not False:
                # Keep track of the last board that won
                lastWinners = winningCards
                lastWinningBall = bingoBall              

        # After all bingo is played, check the last winning board
        # We might have more than one winner
        for cardID in lastWinners:
            # We score based on sum of unmarked (0) spaces
            score = self.sumBoard(cardID,0) * lastWinningBall
            print(f"Last BINGO on card: {cardID} with score: {score}")

    def markCards(self,ballNumber):
        # Loop through each column in each row of each card
        for cardID in range(len(self.bingoBoards)):
            for row in range(len(self.bingoBoards[cardID])):
                for column in range(len(self.bingoBoards[cardID][row])):
                    # Check if the bingo card has a matching number and hasn't already got bingo
                    if self.bingoBoards[cardID][row][column] == ballNumber and cardID not in self.winningBoards:
                        # Mark the corresponding board
                        self.boardMarkers[cardID][row][column] = 1

    def checkBingo(self):
        # Multiple boards can get Bingo at the same time, so need to return a list
        bingoCards = []

        # If the sum of a row or column equals the size of the row/column, then all places are marked (BINGO!)
        for cardID in range(len(self.boardMarkers)):
            numRows, numCols = self.boardMarkers[cardID].shape

            for row in range(numRows):
                # Check for bingo only only if the card hasn't already got bingo
                if sum(self.boardMarkers[cardID][row])==numRows and cardID not in self.winningBoards:
                    # BINGO! - return with the winning card number and mark the board as a winner
                    self.winningBoards.append(cardID)
                    bingoCards.append(cardID)

            for column in range(numCols):
                # Check for bingo only only if the card hasn't already got bingo
                if sum(self.boardMarkers[cardID][:,column])==numCols and cardID not in self.winningBoards:
                    # BINGO! - return with the winning card number and mark the board as a winner
                    self.winningBoards.append(cardID)
                    bingoCards.append(cardID)
        
        # Return list of winning cards, if any
        if len(bingoCards) > 0:
            return bingoCards

        # If no bingo, return false
        return False

    def sumBoard(self,cardID,markCriteria):
        sum = 0
        # Loop through each column in each row of the card
        for row in range(len(self.bingoBoards[cardID])):
            for column in range(len(self.bingoBoards[cardID][row])):
                # Check if the bingo card position matches our mark criteria
                if self.boardMarkers[cardID][row][column] == markCriteria:
                    # Add the number in that position to our sum (score)
                    sum = sum + self.bingoBoards[cardID][row][column]
        return sum

if __name__ == "__main__":
    day4()
