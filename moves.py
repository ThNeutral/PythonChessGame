from typing import List

def pawnMove(x: int, y: int, field: List[List[str]]):
    temp = field[x+1][y]
    field[x+1][y] = field[x][y]
    field[x][y] = temp
    field[x+1][y] = field[x+1][y].split(" ")[0]
    return field