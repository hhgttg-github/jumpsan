
import pyxel
import sprite.sprite as sp
import tile as tl

####====================================
#### CONSTANT

JS_WIDTH  = 8
JS_HEIGHT = 8
JS_W_EDGE = 7

TOPLEFT  = (0,0)
TOPRIGHT = (7,0)
BTMLEFT  = (0,7)
BTMRIGHT = (7,7)

TOP_SIDE_L = (0,-1)
TOP_SIDE_R = (7,-1)
BTM_SIDE_L = (0, 8)
BTM_SIDE_R = (7, 8)

LEFT_SIDE_T  = (-1, 0)
LEFT_SIDE_B  = (-1, 7)
RIGHT_SIDE_T = ( 8, 0)
RIGHT_SIDE_B = ( 8, 7)

TOP_CENTER1 = (3,0)
TOP_CENTER2 = (4,0)
BTM_CENTER1 = (3,7)
BTM_CENTER2 = (4,7)
UNDER_CENTER1 = (3,8)
UNDER_CENTER2 = (4,8)

def plus_tuple(x,y,t):
    return(x+t[0],y+t[1])

# STATES

LEFT  = 0b000000
RIGHT = 0b000001

STOP_L = 0b000000
STOP_R = 0b000001
RUN_L  = 0b001000
RUN_R  = 0b001001
JUMP_L = 0b010000
JUMP_R = 0b010001
FALL_L = 0b011000
FALL_R = 0b011001
LAD_UP = 0b100000
LAD_DN = 0b100001

STOP_MASK = 0b000000
RUN_MASK  = 0b001000
FALL_MASK = 0b011000
LR_MASK   = 0b000001
UD_MASK   = 0b000001
LAD_MASK  = 0b100000

JUMPABLE = [STOP_L,STOP_R,RUN_L,RUN_R]

HRZ_MOVE = 1000 # HORIZONTAL MOVE 横方向移動量
VRT_MOVE = 1000

FALL_Y_MAX = 1000       #落下の最高速度　これ以上は加速しない

####====================================

class Jsan:

    def __init__(self):
        self.sp = sp.AniSprite(0,0,0,0,2,STOP_L,sp.sp8Group)

        self.states = STOP_L

        self.sp.add_frame(STOP_L ,[0],0,(0,0))
        self.sp.add_frame(RUN_L  ,[1,2,3,2],3,(HRZ_MOVE*(-1),None))
        self.sp.add_frame(JUMP_L ,[8],0,None)
        self.sp.add_frame(FALL_L ,[8],0,(None,VRT_MOVE))
        self.sp.add_frame(STOP_R ,[4],0,(0,0))
        self.sp.add_frame(RUN_R  ,[5,6,7,6],3,(HRZ_MOVE,0))
        self.sp.add_frame(JUMP_R ,[9],0,None)
        self.sp.add_frame(FALL_R ,[9],0,(None,VRT_MOVE))
        self.sp.add_frame(LAD_UP ,[10,11],3,(0,VRT_MOVE*(-1)))
        self.sp.add_frame(LAD_DN ,[10,11],3,(0,VRT_MOVE))

####------------------------------------

    def get_direction(self):
        return(self.states & LR_MASK)
    
    def on_ladder(self):
        return(self.states & LAD_MASK)

    def is_falling(self):
        return(self.states & FALL_MASK)
    
####------------------------------------

    def stop_horizontal_move(self):
        print("stop_horizontal")
        if self.is_falling():
            self.sp.dx = 0
            if self.can_stand():
                self.stop_fall()    
        else:
            self.states = STOP_MASK | self.get_direction()
        self.sp.set_frame(self.states)

####------------------------------------

    def run_horizontal(self,dir):
        self.states = RUN_MASK | dir
        self.sp.set_frame(self.states)

####------------------------------------

    def move_vertical(self):
        pass

    def stop_vertical_move(self):
        self.sp.dy = 0
        self.states = STOP_MASK | self.get_direction()
        self.sp.set_frame(self.states)


        # if self.direction == UP:
        #     if not(self.is_passable(UP)):
        #         self.states = STOP
        #     elif self.check_ladder(UP):
        #         self.direction = UP
        #         self.states = LAD
        # if self.direction == DOWN:
        #     if not(self.is_passable(DOWN)):
        #         self.states = STOP
        #     elif self.check_ladder(DOWN):
                
####------------------------------------

    def start_fall(self):
        print("start_fall")
        self.states = FALL_MASK | self.get_direction()
        self.sp.set_frame(self.states)

    def stop_fall(self):
        self.dy = 0

####------------------------------------

    def update(self):

        self.check_corner() #revert_xy含む

        if pyxel.btn(pyxel.KEY_A):
            self.run_horizontal(LEFT)
        elif pyxel.btn(pyxel.KEY_D):
            self.run_horizontal(RIGHT)
        elif (pyxel.btnr(pyxel.KEY_A)) or (pyxel.btnr(pyxel.KEY_D)):
            self.stop_horizontal_move()
        
        # if pyxel.btn(pyxel.KEY_W):
        #     self.move_vertical(LAD_UP)
        # elif pyxel.btn(pyxel.KEY_S):
        #     self.move_vertical(LAD_DN)
        # elif pyxel.btnr(pyxel.KEY_W) or pyxel.btnr(pyxel.KEY_S):
        #     self.stop_vertical_move()

        if self.is_freefall():
            self.start_fall()
        elif self.is_falling and self.can_stand():
            self.check_corner()
            self.stop_fall()
        
        #### ここで必ず上下左右をチェックしてアップデート可能かを調べる。
        #### dx,dy,statesなどの修正をしてから、最終アップデートを！


        self.sp.update()

####------------------------------------

    def draw(self):
        self.sp.draw()
        
####====================================

    def is_freefall(self):
        """落下開始にするかどうか"""
        if self.check_ladder() or self.can_stand():   #梯子に掴まっている・立っているなら、
            return(False)
        else:
            return(True)
        #     x1,y1 = plus_tuple(self.sp.x,self.sp.y,BTM_SIDE_L)
        #     x2,y2 = plus_tuple(self.sp.x,self.sp.y,BTM_SIDE_R)
        #     if tl.is_space(x1,y1) and tl.is_space(x2,y2):
        #        return(True)
        # else:
        #    return(False)
    
    def is_falling(self):
        if (self.states & FALL_MASK):
            return(True)
        else:
            return(False)
    
    def can_stand(self):
        x1,y1 = plus_tuple(self.sp.x,self.sp.y,BTM_SIDE_L)
        x2,y2 = plus_tuple(self.sp.x,self.sp.y,BTM_SIDE_R)
#        x3,y3 = plus_tuple(self.sp.x,self.sp.y,UNDER_CENTER1)
#        x4,y4 = plus_tuple(self.sp.x,self.sp.y,UNDER_CENTER2)
#        if tl.can_stand(x1,y1) or tl.can_stand(x2,y2) or tl.can_stand(x3,y3) or tl.can_stand(x4,y4):
        if tl.can_stand(x1,y1) or tl.can_stand(x2,y2):
            return(True)
        else:
            return(False)
        
    def is_passable(self):
        """ 上下左右が壁で移動できなければならFalseを返す。
            壁以外で移動可能ならならTrueを返す"""
        if self.get_direction() == LEFT:
            x1,y1 = plus_tuple(self.sp.x,self.sp.y,LEFT_SIDE_T)
            x2,y2 = plus_tuple(self.sp.x,self.sp.y,LEFT_SIDE_B)
            if tl.is_passable(x1,y1) and tl.is_passable(x2,y2):
                return(True)
            else:
                return(False)
        elif self.get_direction() == RIGHT:
            x1,y1 = plus_tuple(self.sp.x,self.sp.y,RIGHT_SIDE_T)
            x2,y2 = plus_tuple(self.sp.x,self.sp.y,RIGHT_SIDE_B)
            if tl.is_passable(x1,y1) and tl.is_passable(x2,y2):
                return(True)
            else:
                return(False)
        elif self.states == LAD_UP:
            x1,y1 = plus_tuple(self.sp.x,self.sp.y,TOP_SIDE_L)
            x2,y2 = plus_tuple(self.sp.x,self.sp.y,TOP_SIDE_R)
            if tl.is_wall(x1,y1) or tl.is_wall(x2,y2):
                return(False)
            else:
                return(True)
        elif self.states == LAD_DN:
            x1,y1 = plus_tuple(self.sp.x,self.sp.y,BTM_SIDE_L)
            x2,y2 = plus_tuple(self.sp.x,self.sp.y,BTM_SIDE_R)
            if tl.is_wall(x1,y1) or tl.is_wall(x2,y2):
                return(False)
            else:
                return(True)
            
    def check_ladder(self):
        """上下移動可能ならTrue, できなければFalse"""
        x1,y1 = plus_tuple(self.sp.x,self.sp.y,BTM_CENTER1)
        x2,y2 = plus_tuple(self.sp.x,self.sp.y,BTM_CENTER2)
        x3,y3 = plus_tuple(self.sp.x,self.sp.y,TOP_CENTER1)
        x4,y4 = plus_tuple(self.sp.x,self.sp.y,TOP_CENTER2)

        if (tl.is_ladder(x1,y1) and tl.is_ladder(x2,y2)) or (tl.is_ladder(x3,y3) and tl.is_ladder(x4,y4)):
            return(True)
        else:
            return(False)

####====================================

    def check_corner(self):
        revert=False
        for i in (TOPLEFT,TOPRIGHT,BTMLEFT,BTMRIGHT):
            cx,cy = plus_tuple(self.sp.x,self.sp.y, i)
            if tl.is_wall(cx,cy):
                revert = True
        if revert:
            self.sp.revert_xy()

        
