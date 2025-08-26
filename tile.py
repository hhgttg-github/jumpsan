
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

CAN_STAND = (T_WALL,T_LADDER)
BLOCKED   = (T_WALL)

####==============================================
#### FUNCTION

def get_tile(x,y):
    tl = pyxel.tilemaps[0].pget(x // 8, y // 8)
    return(TILE_DICT.get(tl, T_NONE))

def can_stand(x,y):
    if get_tile(x,y) in CAN_STAND:
        return(True)
    else:
        return(False)

def can_pass(x,y):
    if get_tile(x,y) == T_WALL:
        return(False)
    else:
        return(True)
    
