from pygame import image, transform
import glob


#Funcs
def get_image(pathname: str):
    return image.load(pathname)
        

def get_images(pathname: str):
    arr = []
    for filename in glob.glob(pathname):
        img = transform.scale(image.load(filename), (SIZE_OF_ONE_RECT, SIZE_OF_ONE_RECT))
        arr.append(img)
    return arr

def Reverse(tuples: tuple):
    return tuples[::-1]


#Consts
SCREEN_WIDTH = 720
NUMBER_OF_ROWS = 8
SIZE_OF_ONE_RECT = int(SCREEN_WIDTH / NUMBER_OF_ROWS)

BLACK_SQUARE_COLOR = (55, 55, 55)
HIGHLIGHT_SQUARE_COLOR = (150, 150, 150)
WHITE_SQUARE_COLOR = (200, 200, 200)

ICON = get_image("images/icon/xdd.png")

PIECES_IMAGES = get_images("images/pieces/*.png")

DICT_OF_PIECES_KEYS = {
    "whitepawn": 0,
    "whiterook": 1,
    "whiteknight": 2,
    "whitebishop": 3,
    "whiteking": 4,
    "whitequeen": 5,
    "blackpawn": 6,
    "blackrook": 7,
    "blackknight": 8,
    "blackbishop": 9,
    "blackking": 10,
    "blackqueen": 11,
    "whitepawn highlight": 0,
    "whiterook highlight": 1,
    "whiteknight highlight": 2,
    "whitebishop highlight": 3,
    "whiteking highlight": 4,
    "whitequeen highlight": 5,
    "blackpawn highlight": 6,
    "blackrook highlight": 7,
    "blackknight highlight": 8,
    "blackbishop highlight": 9,
    "blackking highlight": 10,
    "blackqueen highlight": 11
}

field = [["blackrook", "blackknight", "blackbishop", "blackking", "blackqueen", "blackbishop", "blackknight", "blackrook"], 
        ["blackpawn", "blackpawn", "blackpawn", "blackpawn", "blackpawn", "blackpawn", "blackpawn", "blackpawn"],
        ["none", "none", "none", "none", "none", "none", "none", "none"],
        ["none", "none", "none", "none", "none", "none", "none", "none"],
        ["none", "none", "none", "none", "none", "none", "none", "none"],
        ["none", "none", "none", "none", "none", "none", "none", "none"],
        ["whitepawn", "whitepawn", "whitepawn", "whitepawn", "whitepawn", "whitepawn", "whitepawn", "whitepawn"],
        ["whiterook", "whiteknight", "whitebishop", "whitequeen", "whiteking",  "whitebishop", "whiteknight", "whiterook"]]