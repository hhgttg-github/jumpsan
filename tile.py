
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

def is_wall(x,y):
    if get_tile(x,y) == T_WALL:
        return(True)
    else:
        return(False)
    
def is_not_wall(x,y):
    if not(get_tile(x,y) == T_WALL):
        return(True)
    else:
        return(False)

def is_ladder(x,y):
    if get_tile(x,y) == T_LADDER:
        return(True)
    else:
        return(False)
    
def can_ud(x1,y1,x2,y2):
    if is_wall(x1,y1) or is_wall(x2,y2):
        return(False)
    elif is_ladder(x1,y1) or is_ladder(x2,y2):
        return(True)
    else:
        return(False)
    
def is_space(x,y):
    if get_tile(x,y) == T_NONE:
        return(True)
    else:
        return(False)