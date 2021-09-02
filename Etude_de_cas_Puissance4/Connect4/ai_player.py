from player import Player
from game import Game
import math
import random
import copy

import logging

class AIPlayer(Player):
    """This player should implement a heuristic along with a min-max and alpha
    beta search to """
	
    def __init__(self):
        self.name = "VenusAI"

    def getColumn(self, board):
        depth = 4 
        return self.alphaBetaMinMax(board, depth, -math.inf, math.inf, True)[0]     
    
    def alphaBetaMinMax(self, board, depth, alpha, beta, maximizing):
        possibleColumns = board.getPossibleColumns()
        # Base Case
        if self.isTerminal(board): 
            if self.checkWinningSituation(board, self.color):
                return (None, math.inf)
            elif self.checkWinningSituation(board, self.color*(-1)):
                return (None, -math.inf)
            else: # Draw
                return (None, 0)
        if depth == 0:
            return (None, self.scoring(board))
        if maximizing:
            value = -math.inf
            columnToPick = random.choice(possibleColumns)
            for column in possibleColumns:
                boardCopy = copy.deepcopy(board)
                boardCopy.play(self.color, column)
                score = self.alphaBetaMinMax(boardCopy, depth-1, alpha, beta, False)[1]
                if score > value:
                    value = score
                    columnToPick = column
                #elif score == value: 
                #    prob = random.random()
                #    if prob > 0.5 :
                #        value = score
                #        columnToPick = column
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return columnToPick, value
        else: #Min
            value = math.inf
            columnToPick = random.choice(possibleColumns)
            for column in possibleColumns:
                boardCopy = copy.deepcopy(board)
                boardCopy.play(self.color*(-1), column)
                score = self.alphaBetaMinMax(boardCopy, depth-1, alpha, beta, True)[1]
                if score < value:
                    value = score
                    columnToPick = column
                #elif score == value: 
                #    prob = random.random()
                #    if prob > 0.5 :
                #        value = score
                #        columnToPick = column
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return columnToPick, value
    

    def cost(self, subArray, player):
        score = 0
        if subArray.count(player) == 4:
            score += 10000
        elif subArray.count(player) == 3 and subArray.count(0) == 1: 
            score += 5
        elif subArray.count(player) == 2 and subArray.count(0) == 2:
            score += 4
        if subArray.count(player*(-1)) == 3 and subArray.count(0) == 1:
            score -= 5
        elif subArray.count(player*(-1)) == 2 and subArray.count(0) == 2:
            score -= 4
        elif subArray.count(player*(-1)) == 4:
            score -= 10000
        return score

    def scoring(self, board):
        score = 0
        # Center column 
        middleColumnArray = [int(i) for i in list(board[3])]
        middleCount = middleColumnArray.count(self.color)
        score += middleCount*2
        #Vertical
        for column in range(5):
            columnArray = [int(i) for i in list(board[column])]
            for row in range(3):
                subRow = columnArray[row: row+4]
                score += self.cost(subRow, self.color)
        #Horizontal
        for row in range(6):
            rowArray = []
            for i in range(5): 
                rowArray.append(board[i][row])
            for column in range(2):
                subColumn = rowArray[column: column+4]
                score += self.cost(subColumn, self.color)
        # Diagonal positive
        for row in range(3):
            for column in range(2):
                sub = [board[column+i][row+i] for i in range(4)]
                score += self.cost(sub, self.color)
        # Diagonal negative
        for row in range(3):
            for column in range(2):
                sub = [board[column+i][row+3-i] for i in range(4)]
                score += self.cost(sub, self.color)
        return score

    def isTerminal(self, board):
        return (len(board.getPossibleColumns()) == 0 or
            self.checkWinningSituation(board, self.color) or
            self.checkWinningSituation(board, self.color*(-1)))

    def checkWinningSituation(self, board, color):
        # Check Horizontal
        for column in range(4):
                for row in range(6):
                    if board[column][row] == color and board[column+1][row] == color and board[column+2][row] == color and board[column+3][row] == color:
                        return True
        # Check positive Diagonal
        for column in range(4):
            for row in range(3):
                if board[column][row] == color and board[column+1][row+1] == color and board[column+2][row+2] == color and board[column+3][row+3] == color:
                    return True
        # Check negative Diagonal
        for column in range(4):
            for row in range(3, 6):
                if board[column][row] == color and board[column+1][row-1] == color and board[column+2][row-2] == color and board[column+3][row-3] == color:
                    return True
        # Check Vertical
        for column in range(7):
                for row in range(3):
                    if board[column][row] == color and board[column][row+1] == color and board[column][row+2] == color and board[column][row+3] == color:
                        return True

    