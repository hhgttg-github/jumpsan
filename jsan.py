
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
BTM_CENTER1 = (3,8)
BTM_CENTER2 = (4,8)

def plus_tuple(x,y,t):
    return(x+t[0],y+t[1])

# STATES

LEFT = 0b00000
RIGHT = 0b00001
UP    = 0b00010
DOWN  = 0b00011

STOP = 0b00000
RUN  = 0b00100
JUMP = 0b01000
FALL = 0b01100
LAD  = 0b10000

JUMPABLE = [STOP,RUN]

HRZ_MOVE = 1000 # HORIZONTAL MOVE 横方向移動量
VRT_MOVE = 1000

FALL_Y_MAX = 1000       #落下の最高速度　これ以上は加速しない

####====================================

class Jsan:

    def __init__(self):
        self.sp = sp.AniSprite(0,0,0,0,2,STOP+LEFT,sp.sp8Group)
        self.base = self.sp.y + self.sp.h
        
        self.direction = LEFT
        self.states = STOP
        self.v_speed = 0

        self.sp.add_frame(STOP+LEFT ,[0],0,(0,0))
        self.sp.add_frame(RUN+LEFT  ,[1,2,3,2],3,(HRZ_MOVE*(-1),0))
        self.sp.add_frame(JUMP+LEFT ,[8],0,None)
        self.sp.add_frame(FALL+LEFT ,[8],0,None)
        self.sp.add_frame(STOP+RIGHT,[4],0,(0,0))
        self.sp.add_frame(RUN+RIGHT ,[5,6,7,6],3,(HRZ_MOVE,0))
        self.sp.add_frame(JUMP+RIGHT,[9],0,None)
        self.sp.add_frame(FALL+RIGHT,[9],0,None)
        self.sp.add_frame(LAD+LEFT  ,[0],0,(0,0))
        self.sp.add_frame(LAD+RIGHT ,[0],0,(0,0))
        self.sp.add_frame(LAD+UP    ,[10,11],3,(0,VRT_MOVE*(-1)))
        self.sp.add_frame(LAD+DOWN  ,[10,11],3,(0,VRT_MOVE))

####------------------------------------

    def stop_move(self):
        self.direction = LEFT
        self.states = STOP

####------------------------------------

    def run_horizontal(self,dir):
        if dir == LEFT:
            if not(self.check_wall(LEFT)):
                self.direction = dir
                self.states = RUN
        elif dir == RIGHT:
            if not(self.check_wall(RIGHT)):
                self.direction = dir
                self.states = RUN

####------------------------------------

    def move_vertical(self,dir):
        if self.check_ladder(UP) and (dir == UP):
                self.direction = UP
                self.states = LAD
        elif self.check_ladder(DOWN) and (dir == DOWN):
                self.direction = DOWN
                self.states = LAD
    
####------------------------------------

    def start_fall(self):
        self.states = FALL
        self.sp.dy = FALL_Y_MAX

    def stop_fall(self):
        self.states = STOP
        self.sp.dy = 0

####------------------------------------

    def update(self):

        if pyxel.btn(pyxel.KEY_A):
            self.run_horizontal(LEFT)
        elif pyxel.btn(pyxel.KEY_D):
            self.run_horizontal(RIGHT)
        elif (pyxel.btnr(pyxel.KEY_A)) or (pyxel.btnr(pyxel.KEY_D)):
            self.stop_move()
        
        if pyxel.btn(pyxel.KEY_W):
            self.move_vertical(UP)
        elif pyxel.btn(pyxel.KEY_S):
            self.move_vertical(DOWN)
        elif pyxel.btnr(pyxel.KEY_W) or pyxel.btnr(pyxel.KEY_S):
            self.stop_move()

        self.sp.set_frame(self.states + self.direction)
        #### ここで必ず上下左右をチェックしてアップデート可能かを調べる。
        #### dx,dy,statesなどの修正をしてから、最終アップデートを！
        
        if (self.states == FALL) and (self.can_stand()):
            self.stop_fall()
        
        if self.is_freefall():
            self.start_fall()

        #左右が壁なら左右移動中止
        if self.sp.dx > 0:
            if self.check_wall(RIGHT):
                self.sp.dx = 0
        elif self.sp.dx < 0:
            if self.check_wall(LEFT):
                self.sp.dx = 0

        #落下中、下が壁/梯子なら下移動中止
        if self.states == FALL:
            if self.check_wall(DOWN) or self.check_ladder(DOWN):
                self.stop_fall()

        #上下移動中、上下が壁なら停止
        if self.sp.dy > 0 and self.check_wall(DOWN):
                self.stop_move()
        elif self.sp.dy < 0 and self.check_wall(UP):
                self.stop_move()

        self.sp.update()

####------------------------------------

    def draw(self):
        self.sp.draw()
        
####====================================

    def is_freefall(self):
        """足元が空間で落下するかどうか"""
        x1,y1 = plus_tuple(self.sp.x,self.sp.y,BTM_SIDE_L)
        x2,y2 = plus_tuple(self.sp.x,self.sp.y,BTM_SIDE_R)
        if tl.is_space(x1,y1) and tl.is_space(x2,y2):
            return(True)
        else:
            return(False)
        
    def can_stand(self):
        """足元が床/梯子で立つことができればTrue
            落下するならFalse"""
        x1,y1 = plus_tuple(self.sp.x,self.sp.y,BTM_SIDE_L)
        x2,y2 = plus_tuple(self.sp.x,self.sp.y,BTM_SIDE_R)
        if (tl.can_stand(x1,y1)) or (tl.can_stand(x2,y2)):
            return(True)
        else:
            return(False)
        
    def check_wall(self,dir):
        """ 上下左右が壁で移動不可能ならTrueを返す。
            移動可能ならFalseを返す"""
        if dir == LEFT:
            x1,y1 = plus_tuple(self.sp.x,self.sp.y,LEFT_SIDE_T)
            x2,y2 = plus_tuple(self.sp.x,self.sp.y,LEFT_SIDE_B)
            if tl.can_pass(x1,y1) and tl.can_pass(x2,y2):
                return(False)
            else:
                return(True)
        if dir == RIGHT:
            x1,y1 = plus_tuple(self.sp.x,self.sp.y,RIGHT_SIDE_T)
            x2,y2 = plus_tuple(self.sp.x,self.sp.y,RIGHT_SIDE_B)
            if tl.can_pass(x1,y1) and tl.can_pass(x2,y2):
                return(False)
            else:
                return(True)
        if dir == UP:
            x1,y1 = plus_tuple(self.sp.x,self.sp.y,TOP_SIDE_L)
            x2,y2 = plus_tuple(self.sp.x,self.sp.y,TOP_SIDE_R)
            if tl.is_wall(x1,y1) or tl.is_wall(x2,y2):
                return(True)
            else:
                return(False)
        if dir == DOWN:
            x1,y1 = plus_tuple(self.sp.x,self.sp.y,BTM_SIDE_L)
            x2,y2 = plus_tuple(self.sp.x,self.sp.y,BTM_SIDE_R)
            if tl.is_wall(x1,y1) or tl.is_wall(x2,y2):
                return(True)
            else:
                return(False)
            
    def check_ladder(self,dir):
        """上下移動可能ならTrue, できなければFalse"""
        if dir == UP:
            x1,y1 = plus_tuple(self.sp.x,self.sp.y,TOP_CENTER1)
            x2,y2 = plus_tuple(self.sp.x,self.sp.y,TOP_CENTER2)
            if tl.is_ladder(x1,y1) and tl.is_ladder(x2,y2):
                return(True)
            else:
                return(False)
        elif dir == DOWN:
            x1,y1 = plus_tuple(self.sp.x,self.sp.y,BTM_CENTER1)
            x2,y2 = plus_tuple(self.sp.x,self.sp.y,BTM_CENTER2)
            if tl.is_ladder(x1,y1) and tl.is_ladder(x2,y2):
                return(True)
            else:
                return(False)
