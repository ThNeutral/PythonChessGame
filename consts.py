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
    new_tup = tuples[::-1]
    return new_tup


#Consts
SCREEN_WIDTH = 720
NUMBER_OF_ROWS = 8
SIZE_OF_ONE_RECT = int(SCREEN_WIDTH / NUMBER_OF_ROWS)

BLACK_SQUARE_COLOR = (55, 55, 55)
WHITE_SQUARE_COLOR = (200, 200, 200)

ICON = get_image("images/icon/xdd.png")

PIECES_IMAGES = get_images("images/pieces/*.png")

DICT_OF_PIECES_KEYS = {
    "wpawn": 0,
    "wrook": 1,
    "wknight": 2,
    "wbishop": 3,
    "wking": 4,
    "wqueen": 5,
    "bpawn": 6,
    "brook": 7,
    "bknight": 8,
    "bbishop": 9,
    "bking": 10,
    "bqueen": 11
}

FIELD = (("brook", "bknight", "bbishop", "bking", "bqueen", "bbishop", "bknight", "brook"), 
        ("bpawn", "bpawn", "bpawn", "bpawn", "bpawn", "bpawn", "bpawn", "bpawn"),
        ("none", "none", "none", "none", "none", "none", "none", "none"),
        ("none", "none", "none", "none", "none", "none", "none", "none"),
        ("none", "none", "none", "none", "none", "none", "none", "none"),
        ("none", "none", "none", "none", "none", "none", "none", "none"),
        ("wpawn", "wpawn", "wpawn", "wpawn", "wpawn", "wpawn", "wpawn", "wpawn"),
        ("wrook", "wknight", "wbishop", "wqueen", "wking",  "wbishop", "wknight", "wrook"))