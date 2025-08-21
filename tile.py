
import pyxel

####==============================================
#### CONSTANT

T_NONE = 0
T_WALL = 1
T_LADDER = 2
T_EXIT = 3

####==============================================
#### VARIABLES

TILE_DICT = {
    (0,0) : T_WALL,
    (1,0) : T_LADDER,
    (0,1) : T_EXIT
}

####==============================================
#### FUNCTION

def get_tile(x,y):
    tl = pyxel.tilemap[0].pget(x // 8, y // 8)
    return(TILE_DICT.get(tl, T_NONE))