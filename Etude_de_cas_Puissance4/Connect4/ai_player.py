from player import Player

class AIPlayer(Player):
    """This player should implement a heuristic along with a min-max and alpha
    beta search to """
	
    def __init__(self):
        self.name = "VenusAI"

    
    def getColumn(self, board):
         # TODO(student): implement this!
        return 0

    def miniMax(self):
        return 0
    
    def alphaBeta(self):
        return 0
    

    def cost(self, subArray, player):
        score = 0
        if subArray.count(player) == 4:
            score += 16
        elif subArray.count(player) == 3 and subArray.count(0) == 1: 
            score += 8
        elif subArray.count(player) == 2 and subArray.count(0) == 2:
            score += 4
        if subArray.count(player*(-1)) == 3 and subArray.count(0) == 1:
            score += 8
        return score

    def scoring(self, board):
        score = 0 
        # Center column 
        middleColumnArray = [int(i) for i in list(board[:, 3])]
        middleCount = middleColumnArray.count(self.color)
        score += middleCount*4
        #Vertical
        for column in range(5):
            columnArray = [int(i) for i in list(board[:,column])]
            for row in range(3):
                subRow = columnArray[row: row+4]
                score += self.cost(subRow, self.color)
        #Horizontal
        for row in range(6):
            rowArray = [int(i) for i in list(board[row,:])]
            for column in range(2):
                subColumn = rowArray[column: column+4]
                score += self.cost(subColumn, self.color)
        # Diagonal positive 
        for row in range(3):
            for column in range(2):
                sub = [board[row+i][column+i] for i in range(4)]
                score += self.cost(sub, self.color)
        # Diagonal negative 
        for row in range(3):
            for column in range(2):
                sub = [board[row+3-i][column+i] for i in range(4)]
                score += self.cost(sub, self.color)
        return score

    def isTerminal(self, board, game):
        possibleColumns = board.getPossibleColumns()
        if possibleColumns == 0: 
            return True
        else:
            result = False 
            for possibleColumn in range(possibleColumns):
                for possibleRow in range(board.getHeight(possibleColumn), 5):
                    possiblePosition = [possibleColumn, possibleRow]
                    if (game.getWinner(possiblePosition) == None or 
                        game.getWinner(possiblePosition) == True or 
                        game.getWinner(possiblePosition) == False):
                        result = True
                        break
                if result:
                    break
            return result                             
