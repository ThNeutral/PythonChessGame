from pygame import image, transform, Surface

#Classes
#----------------------------------------------------------------------------------------------------

class Board:
    def __init__(self, fen: str):
        self.square = self.loadFromFEN(fen)
        self.colourToMove = fen.split(" ")[1]
        self.numColorToMove = 0 if fen.split(" ")[1] == "w" else 1
        self.numSquaresToEdges = self.precomputedMoveData()
        self.moves = self.generateMoves()

    def precomputedMoveData(self):
        numSquaresToEdges = [None] * 64
        for file in range(8):
            for rank in range(8):
             numSquaresToEdges[rank * 8 + file] = [
                7 - rank,
                rank,
                file,
                7 - file,
                min(7 - rank, file),
                min(rank, 7 - file),
                min(7 - rank, 7 - file),
                min(rank, file)
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
        moves = []
        for startSquare in range(len(self.square)):
            piece = self.square[startSquare]
            if piece != None:
                if is_set(piece, 5) == self.numColorToMove:
                    if piece in SLIDING_PIECES:
                        moves = self.generateSlidingPieceMove(startSquare, piece, moves)
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
        return moves

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

SLIDING_PIECES = [12, 13, 14, 20, 21, 22]

BISHOP = [12, 20]
ROOK = [13, 21]

fen = "rnbqkbnr/8/8/8/8/8/8/RNBQKBNR w KQkq - 0 1"

board = Board(fen)