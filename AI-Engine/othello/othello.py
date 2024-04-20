import math
import random
import sys
import copy

EMPTY = 2
PLAYER1 = 0
PLAYER2 = 1
PLAYER_NAMES = ["O", "X", "."]
OTHER_PLAYER = {PLAYER1:PLAYER2, PLAYER2:PLAYER1}

class OthelloMove:
    def __init__(self, player , x , y ):
        self.player = player
        self.x = x
        self.y = y
    
    def __str__(self):
        return "Player " + PLAYER_NAMES[self.player] + " to " + str(self.x) + "," + str(self.y)


class State:
    def __init__(self, board = None, boardSize = 8, nextPlayerToMove = PLAYER1):
        
        if board:
            self.board = board
            self.boardSize = boardSize
            self.nextPlayerToMove =  nextPlayerToMove
        
        # This will creates a board with the initial state for the game of Othello
        else:
            self.boardSize = boardSize
            if boardSize < 2 :
                self.boardSize = 2
            self.nextPlayerToMove =  nextPlayerToMove
            
            self.board = [[EMPTY] * boardSize for y in range(boardSize)]
            #  initial position:
            self.board[boardSize//2-1][boardSize//2-1] = PLAYER1
            self.board[boardSize//2][boardSize//2] = PLAYER1
            self.board[boardSize//2-1][boardSize//2] = PLAYER2
            self.board[boardSize//2][boardSize//2-1] = PLAYER2
    
    # Converts a game board to a string, for displaying it via the console
    def __str__(self):
        output = ""
        for i in range(self.boardSize):
            for j in range(self.boardSize):
                output += PLAYER_NAMES[self.board[i][j]] + " "
            output += "\n"
        return output

    def __eq__(self, state):
        return self.board == state.board

    def clone(self):
        return State(copy.deepcopy(self.board), self.boardSize, self.nextPlayerToMove)

    def is_legal(self, x, y):
        return x >= 0 and x < self.boardSize and y >= 0 and y < self.boardSize

    def get(self, x, y):
        return self.board[y][x] if self.is_legal(x, y) else None

    def row(self, y):
        return self.board[y]

    def num_empties(self):
        return sum(r.count(EMPTY) for r in self.board)


    def equals(self, state):
        return self.board == state.board
    
    # Determines whether the game is over or not
    def game_over(self):
        return len(self.generateMoves(PLAYER1)) == 0 and len(self.generateMoves(PLAYER2)) == 0

    # Returns the final score, once a game is over
    def score(self):
        score = 0
        for i in range(self.boardSize):
            for j in range(self.boardSize):
                if self.board[i][j] == PLAYER1:
                    score += 1
                if self.board[i][j] == PLAYER2:
                    score -= 1
        return score
    
    #  Returns the list of possible moves for player 'player'
    def generateMoves(self, player = None):

        if player == None:
            player = self.nextPlayerToMove
        moves = []

        # these two arrays encode the 8 posible directions in which a player can capture pieces:
        offs_x = [ 0, 1, 1, 1, 0,-1,-1,-1]
        offs_y = [-1,-1, 0, 1, 1, 1, 0,-1]

        for i in range(self.boardSize):
            for j in range(self.boardSize):
                if self.board[i][j] == EMPTY :
                    moveFound = False
                    for k in range(len(offs_x)):
                        if not moveFound:
                            current_x = i + offs_x[k]
                            current_y = j + offs_y[k]
                            while(current_x+offs_x[k]>=0 and current_x+offs_x[k]< self.boardSize and
                                current_y+offs_y[k]>=0 and current_y+offs_y[k]<self.boardSize and
                                self.board[current_x][current_y] == OTHER_PLAYER[player]):
                                current_x += offs_x[k]
                                current_y += offs_y[k]
                                if self.board[current_x][current_y] == player:
                                    #  Legal move:
                                    moveFound = True
                                    moves.append(OthelloMove(player, i, j))
        return moves


     
    # Modifies the game state as for applying the given 'move'
    # Notice that move can be "null", which means that the player passes.
    # "passing" is only allowed if a player has no other moves available.
    def applyMove(self, move):

        if move == None:
            print("\nPlayer " + PLAYER_NAMES[self.nextPlayerToMove] + " passes the move!")
            self.nextPlayerToMove = OTHER_PLAYER[self.nextPlayerToMove]
            return #player passes

        self.nextPlayerToMove = OTHER_PLAYER[self.nextPlayerToMove]
        
        # set the piece:
        self.board[move.x][move.y] = move.player
        
        # these two arrays encode the 8 posible directions in which a player can capture pieces:
        offs_x = [ 0, 1, 1, 1, 0,-1,-1,-1]
        offs_y = [-1,-1, 0, 1, 1, 1, 0,-1]
        
        # see if any pieces are captured:
        for i in range(len(offs_x)):
            current_x = move.x + offs_x[i]
            current_y = move.y + offs_y[i]
            while (current_x+offs_x[i]>=0 and current_x+offs_x[i]<self.boardSize and
                  current_y+offs_y[i]>=0 and current_y+offs_y[i]<self.boardSize and
                  self.board[current_x][current_y] == OTHER_PLAYER[move.player]):
                current_x += offs_x[i]
                current_y += offs_y[i]
                if self.board[current_x][current_y] == move.player : 
                    # pieces captured!:
                    reversed_x = move.x + offs_x[i]
                    reversed_y = move.y + offs_y[i]
                    while reversed_x!=current_x or reversed_y!=current_y :
                        self.board[reversed_x][reversed_y] = move.player
                        reversed_x += offs_x[i]
                        reversed_y += offs_y[i]
                    break

    # Creates a new game state that has the result of applying move 'move'
    def applyMoveCloning(self, move):
        newState = self.clone()
        newState.applyMove(move)
        return newState

    def winner(self):
        if self.score() > 0:
            return PLAYER_NAMES[PLAYER1]
        elif self.score() < 0:
            return PLAYER_NAMES[PLAYER2]
        else:
            return "DRAW"

