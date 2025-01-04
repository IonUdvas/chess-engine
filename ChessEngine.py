import numpy as np

class GameState:
    def __init__(self):
        self.board = np.array([
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ])

        self.moveFunctions = {'P' : self.getPawnMoves,
                              'R' : self.getRookMoves,
                              'N' : self.getKnightMoves,
                              'B' : self.getBishopMoves,
                              'Q' : self.getQueenMoves,
                              'K' : self.getKingMoves}

        self.whiteToMove = True
        self.moveLog = []

        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)

        self.checkMate = False
        self.staleMate = False

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove

        # Kings'location update
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove

    def getValidMoves(self):
        moves = self.getPossibleMoves()

        for m in moves[:]:
            self.makeMove(m)
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(m)
            self.whiteToMove = not self.whiteToMove
            self.undoMove()

        if len(moves) == 0:
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        
        else:
            self.checkMate = False
            self.staleMate = False

        print(self.checkMate)

        return moves
    
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation)
        else:
            return self.squareUnderAttack(self.blackKingLocation)
        
    def squareUnderAttack(self, location):
        self.whiteToMove = not self.whiteToMove
        oppMoves = self.getPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for m in oppMoves:
            if (m.endRow, m.endCol) == location:
                return True
        return False

    def getPossibleMoves(self):
        moves = []
        for r in range(self.board.shape[0]):
            for c in range(self.board.shape[1]):
                turn = self.board[r][c][0]

                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)

        return moves
    
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:
            if self.board[r-1][c] == "--":
                moves.append(Move((r,c), (r-1,c), self.board))
                if r == 6 and self.board[r-2][c] == '--':
                    moves.append(Move((r,c), (r-2, c), self.board))

            if c-1 >= 0:
                if self.board[r-1][c-1][0] == 'b':
                    moves.append(Move((r,c), (r-1, c-1), self.board))
            if c+1 <= self.board.shape[1]-1:
                if self.board[r-1][c+1][0] == 'b':
                    moves.append(Move((r,c), (r-1, c+1), self.board))
        
        else:
            if self.board[r+1][c] == "--":
                moves.append(Move((r,c), (r+1,c), self.board))
                if r == 1 and self.board[r+2][c] == '--':
                    moves.append(Move((r,c), (r+2, c), self.board))

            if c-1 >= 0:
                if self.board[r+1][c-1][0] == 'w':
                    moves.append(Move((r,c), (r+1, c-1), self.board))
            if c+1 <= self.board.shape[1]-1:
                if self.board[r-1][c+1][0] == 'w':
                    moves.append(Move((r,c), (r+1, c+1), self.board))

    def getRookMoves(self, r, c, moves):
        directions = [(-1, 0), (1, 0), (0,1), (0,-1)]
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1,8):
                endRow = d[0] * i + r
                endCol = d[1] * i + c

                if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                    endPiece = self.board[endRow][endCol]

                    if endPiece == '--':
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getKnightMoves(self, r, c, moves):
        directions = [(-2, -1), (-1, -2), (2, -1), (-1, 2), (2, 1), (1,2), (-2, 1), (1, -2)]
        allyColor = "w" if self.whiteToMove else "b"  # Change made to write less code in if statement
        for d in directions:        
                endRow = d[0] + r
                endCol = d[1] + c

                if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                    endPiece = self.board[endRow][endCol]

                    if endPiece[0] != allyColor:
                        moves.append(Move((r,c), (endRow, endCol), self.board))

    def getBishopMoves(self, r, c, moves):
        directions = [(-1, -1), (1, 1), (-1, 1), (1,-1)]
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1,8):
                endRow = d[0] * i + r
                endCol = d[1] * i + c

                if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                    endPiece = self.board[endRow][endCol]

                    if endPiece == '--':
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getKingMoves(self, r, c, moves):
        directions = [(-1, -1), (1, 1), (-1, 1), (1,-1), (-1, 0), (1, 0), (0,1), (0,-1)]
        allyColor = "w" if self.whiteToMove else "b"  # Change made to write less code in if statement
        for d in directions:
            endRow = r + d[0]
            endCol = c + d[1]
            
            if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r,c), (endRow, endCol), self.board))


    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)
 
class Move:
    ranksToRows = {"1" : 7, "2" : 6, "3" : 5, "4" : 4,
                   "5" : 3, "6" : 2, "7" : 1, "8" : 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a" : 0, "b" : 1, "c" : 2, "d" : 3,
                   "e" : 4, "f" : 5, "g" : 6, "h" : 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow, self.startCol = startSq
        self.endRow, self.endCol = endSq

        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]

        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
        
    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
        