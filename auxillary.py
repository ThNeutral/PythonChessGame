from pygame import image, transform, Surface

#Classes
#----------------------------------------------------------------------------------------------------

class Board:
    def __init__(self, fen: str):
        self.square = self.loadFromFEN(fen)
        self.colourToMove = fen.split(" ")[1]
        self.numColorToMove = 0
        self.numSquaresToEdges = self.precomputedMoveData()
        self.win = None
        self.doubleMoves = []
        self.doubleMove = None
        self.castling = [True, True]
        self.castlingMoves = []
        self.moves = self.generateMoves()
        self.toRemove = None

    def precomputedMoveData(self):
        numSquaresToEdges = [[]] * 64
        for file in range(8):
            for rank in range(8):
             north = 7-rank
             south = rank
             west = file
             east = 7 - file

             numSquaresToEdges[rank * 8 + file] = [
                north,
                south,
                west,
                east,
                min(north, west),
                min(south, east),
                min(north, east),
                min(south, west)
             ]
        return numSquaresToEdges
    
    def loadFromFEN(self, fen: str): 
        board: list[None | int] = [None] * 64
        dictionary = {
            "p": DICT_OF_PIECES["pawn"],
            "n": DICT_OF_PIECES["knight"],
            "b": DICT_OF_PIECES["bishop"],
            "r": DICT_OF_PIECES["rook"],
            "q": DICT_OF_PIECES["queen"],
            "k": DICT_OF_PIECES["king"],
        }

        file = 0
        rank = 0

        for char in fen.split(" ")[0]:
            if char == "/":
                file = 0
                rank = rank + 1
            else:
                if char.isnumeric():
                    file = file + int(char)
                else:
                    colour = DICT_OF_PIECES["white"] if char.isupper() else DICT_OF_PIECES["black"]
                    piece = dictionary[char.lower()]
                    board[rank * 8 + file] = colour | piece
                    file = file + 1
    
        return board
    
    def generateMoves(self): 
        self.doubleMoves = []
        self.castlingMoves = []
        moves = []
        if not KING[0] in self.square:
            self.win = "black"
        elif not KING[1] in self.square:
            self.win = "white"
        for startSquare in range(len(self.square)):
            piece = self.square[startSquare]
            if piece != None:
                if (is_set(piece, 4) / 16) == self.numColorToMove:
                    if piece in SLIDING_PIECES:
                        moves = self.generateSlidingPieceMove(startSquare, piece, moves)
                    elif piece in PAWN:
                        moves = self.generatePawnMove(startSquare, piece, moves)
                    elif piece in KNIGHT:
                        moves = self.generateKnightMoves(startSquare, piece, moves)
        if self.numColorToMove == 1:
            self.numColorToMove = 0
        else:
            self.numColorToMove = 1
        return moves

    def generateSlidingPieceMove(self, startSquare: int, piece: int, moves):         
        startDirectionIndex = 4 if piece in BISHOP else 0
        endDirectionIndex = 4 if piece in ROOK else 8
        
        for directionIndex in range(startDirectionIndex, endDirectionIndex):
            for n in range(self.numSquaresToEdges[startSquare][directionIndex]):
                targetSquare = startSquare + DIRECTIONAL_OFFSETS[directionIndex] * (n + 1)
                pieceOnTargetSquare = self.square[targetSquare]

                if is_set_two(piece, pieceOnTargetSquare, 4):
                    break
                    
                moves.append((startSquare, targetSquare))

                if not_is_set_two(piece, pieceOnTargetSquare, 4):
                    break

                if piece in KING:
                    leftCastlingPattern = [[13, None, None, None, 9], [21, None, None, None, 17]]
                    rightCastlingPattern = [[17, None, None, 21], [9, None, None, 13]]
                    if self.castling[0]:
                        row = self.square[56:64]
                        if row[:5] in leftCastlingPattern:
                            moves.append((60, 56))
                            self.castlingMoves.append((60, 56))
                        if row[4:] in rightCastlingPattern:
                            moves.append((60, 63))
                            self.castlingMoves.append((60, 63))

                    if self.castling[1]:
                        row = self.square[:8]
                        if row[:5] in leftCastlingPattern:
                            moves.append((4, 0))
                            self.castlingMoves.append((4, 0))
                        if row[4:] in rightCastlingPattern:
                            moves.append((4, 7))
                            self.castlingMoves.append((4, 7))

                    break
        return moves
    
    def generatePawnMove(self, startSquare: int, piece: int, moves): 
        if is_set(piece, 4):
            startPositions = [8, 9, 10, 11, 12, 13, 14, 15]
            if startSquare in startPositions: 
                directions = [9, 8, 7, 16]
            else:
                directions = [9, 8, 7]
        else:
            startPositions = [48, 49, 50, 51, 52, 53, 54, 55]
            if startSquare in startPositions: 
                directions = [-9, -8, -7, -16]
            else:
                directions = [-9, -8, -7]
        
        for directionIndex in directions:
            targetSquare = startSquare + directionIndex
            pieceOnTargetSquare = self.square[targetSquare]

            if is_set_two(piece, pieceOnTargetSquare, 4):
                continue
            elif not_is_set_two(piece, pieceOnTargetSquare, 4):
                if directionIndex in [-9, -7, 7, 9]:
                    moves.append((startSquare, targetSquare))  
                continue  
            else:
                if directionIndex in [-8, 8]:
                    moves.append((startSquare, targetSquare))
                    if self.doubleMove != None:
                        if (self.doubleMove[0] == startSquare - 8 - 8 - 1) or (self.doubleMove[0] == startSquare - 8 - 8 + 1):
                            moves.append((startSquare, targetSquare + 1))
                            self.toRemove = startSquare + 1
                        if (self.doubleMove[0] == startSquare + 8 + 8 - 1) or (self.doubleMove[0] == startSquare + 8 + 8 + 1):
                            moves.append((startSquare, targetSquare - 1))
                            self.toRemove = startSquare - 1 
                            
                elif directionIndex in [-16, 16]:
                    self.doubleMoves.append((startSquare, targetSquare))
                    moves.append((startSquare, targetSquare))
            
        return moves
    
    def generateKnightMoves(self, startSquare: int, piece: int, moves):
        directions = [8+8+1, 8+8-1, -8-8+1, -8-8-1, -1-1+8, -1-1-8, 1+1+8, 1+1-8]


        for directionIndex in directions:
            targetSquare = startSquare + directionIndex
            if targetSquare < 0 or targetSquare > 63:
                continue
            pieceOnTargetSquare = self.square[targetSquare]

            if is_set_two(piece, pieceOnTargetSquare, 4):
                continue 
            elif self.checkDistanceToBorder(self.numSquaresToEdges[startSquare], directionIndex):
                continue
            else:
                moves.append((startSquare, targetSquare))
            
        return moves   
    
    def checkDistanceToBorder(self, numSquaresToEdges, directionIndex):
        if directionIndex == (8+8+1):
            return (numSquaresToEdges[0] in [0, 1]) or (numSquaresToEdges[3] == 0)
        elif directionIndex == (8+8-1):
            return (numSquaresToEdges[0] in [0, 1]) or (numSquaresToEdges[2] == 0)
        elif directionIndex == (-8-8-1):
            return (numSquaresToEdges[1] in [0, 1]) or (numSquaresToEdges[2] == 0)
        elif directionIndex == (-8-8+1):
            return (numSquaresToEdges[1] in [0, 1]) or (numSquaresToEdges[3] == 0)
        elif directionIndex == (-1-1-8):
            return (numSquaresToEdges[2] in [0, 1]) or (numSquaresToEdges[1] == 0)
        elif directionIndex == (-1-1+8):
            return (numSquaresToEdges[2] in [0, 1]) or (numSquaresToEdges[0] == 0)
        elif directionIndex == (1+1+8):
            return (numSquaresToEdges[3] in [0, 1]) or (numSquaresToEdges[1] == 0)
        elif directionIndex == (1+1-8):
            return (numSquaresToEdges[3] in [0, 1]) or (numSquaresToEdges[0] == 0)


#Funcs
#----------------------------------------------------------------------------------------------------
def get_image(pathname: str):
    return image.load(pathname)

def Reverse(tuples: tuple):
    return tuples[::-1]

def is_set(x, n):
    return x & 1 << n

def is_set_two(x, y, n):
    if (x == None) or (y == None): return False
    return x & 1 << n == y & 1 << n

def not_is_set_two(x, y, n):
    if (x == None) or (y == None): return False
    return x & 1 << n != y & 1 << n

#Consts
#----------------------------------------------------------------------------------------------------
SCREEN_WIDTH = 720
SIZE_OF_ONE_RECT = int(SCREEN_WIDTH / 8)

DIRECTIONAL_OFFSETS = [8, -8, -1, 1, 7, -7, 9, -9]

BLACK_SQUARE_COLOR = (55, 55, 55)
HIGHLIGHT_SQUARE_COLOR = (150, 150, 150)
WHITE_SQUARE_COLOR = (200, 200, 200)

tranparentSurface = Surface((SIZE_OF_ONE_RECT, SIZE_OF_ONE_RECT))
tranparentSurface.set_colorkey((0, 0, 0))

ICON = get_image("images/icon/xdd.png")

PIECES_IMAGES = {
    None: tranparentSurface, 
    8: tranparentSurface,
    16: tranparentSurface,

    9: transform.scale(image.load("images/pieces/whiteKing.png"), (SIZE_OF_ONE_RECT, SIZE_OF_ONE_RECT)),
    10: transform.scale(image.load("images/pieces/whitePawn.png"), (SIZE_OF_ONE_RECT, SIZE_OF_ONE_RECT)),
    11: transform.scale(image.load("images/pieces/whiteKnight.png"), (SIZE_OF_ONE_RECT, SIZE_OF_ONE_RECT)),
    12: transform.scale(image.load("images/pieces/whiteBishop.png"), (SIZE_OF_ONE_RECT, SIZE_OF_ONE_RECT)),
    13: transform.scale(image.load("images/pieces/whiteRook.png"), (SIZE_OF_ONE_RECT, SIZE_OF_ONE_RECT)),
    14: transform.scale(image.load("images/pieces/whiteQueen.png"), (SIZE_OF_ONE_RECT, SIZE_OF_ONE_RECT)),

    17: transform.scale(image.load("images/pieces/blackKing.png"), (SIZE_OF_ONE_RECT, SIZE_OF_ONE_RECT)),
    18: transform.scale(image.load("images/pieces/blackPawn.png"), (SIZE_OF_ONE_RECT, SIZE_OF_ONE_RECT)),
    19: transform.scale(image.load("images/pieces/blackKnight.png"), (SIZE_OF_ONE_RECT, SIZE_OF_ONE_RECT)),
    20: transform.scale(image.load("images/pieces/blackBishop.png"), (SIZE_OF_ONE_RECT, SIZE_OF_ONE_RECT)),
    21: transform.scale(image.load("images/pieces/blackRook.png"), (SIZE_OF_ONE_RECT, SIZE_OF_ONE_RECT)),
    22: transform.scale(image.load("images/pieces/blackQueen.png"), (SIZE_OF_ONE_RECT, SIZE_OF_ONE_RECT)),    
}


DICT_OF_PIECES = {
    "none": 0,
    "king": 1,
    "pawn": 2,
    "knight": 3,
    "bishop": 4,
    "rook": 5,
    "queen": 6,

    "white": 8,
    "black": 16 
}

SLIDING_PIECES = [12, 13, 14, 20, 21, 22, 9, 17]

KING = [9, 17]
PAWN = [10, 18]
KNIGHT = [11, 19]
BISHOP = [12, 20]
ROOK = [13, 21]

default_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"