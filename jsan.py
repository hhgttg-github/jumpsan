
import pyxel
import sprite.sprite as sp
import tile as tl

####====================================
#### CONSTANT

#### SPEED -----------------------------

HRZ_MOVE = 1200 # HORIZONTAL MOVE 横方向移動量
VRT_MOVE = 1200

FALL_Y_MAX = 1000       #落下の最高速度　これ以上は加速しない

#### SIZE -------------------------------

JS_WIDTH  = 8
JS_HEIGHT = 8
JS_W_EDGE = 7

#### AREA -------------------------------

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

# STATES BITs

LEFT  = 0b000000
RIGHT = 0b000001
UP    = 0b000000
DOWN  = 0b000001

STOP_L = 0b000000
STOP_R = 0b000001
RUN_L  = 0b000100
RUN_R  = 0b000101
JUMP_L = 0b001000
JUMP_R = 0b001001
FALL_L = 0b010000
FALL_R = 0b010001
LAD_UP = 0b100000
LAD_DN = 0b100001

STOP_MASK = 0b000000
RUN_MASK  = 0b000100
JUMP_MASK = 0b001000
FALL_MASK = 0b010000
LR_MASK   = 0b000001
UD_MASK   = 0b000001
LAD_MASK  = 0b100000

JUMPABLE = [STOP_L,STOP_R,RUN_L,RUN_R]

#### MASK FUNCTION ---------------------

def is_mask_true(b,m):
    return((b & m) == m)

# def get_direction(self):      ← class JSANの中です。
#     return(self.states & LR_MASK)

####====================================
####
#### JSAN CLASS

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

####------------------------------------

    def update(self):

        if pyxel.btn(pyxel.KEY_A):
            self.run_horizontal(LEFT)
        elif pyxel.btn(pyxel.KEY_D):
            self.run_horizontal(RIGHT)
        elif (pyxel.btnr(pyxel.KEY_A)) or (pyxel.btnr(pyxel.KEY_D)):
            self.stop_horizontal_move()
        
        if pyxel.btn(pyxel.KEY_W):
            self.move_ladder(UP)
        elif pyxel.btn(pyxel.KEY_S):
            self.move_ladder(DOWN)
        elif pyxel.btnr(pyxel.KEY_W) or pyxel.btnr(pyxel.KEY_S):
            if is_mask_true(self.states, LAD_MASK):
                self.stop_vertical_move()

        #### ここで必ず上下左右をチェックしてアップデート可能かを調べる。
        #### dx,dy,statesなどの修正をしてから、最終アップデートを！

        self.check_4corner_wall() #revert_xy含む
        self.check_btm_corner_wall()

        if self.is_falling() and self.can_stand():
             self.stop_fall()
        elif self.is_freefall():
            self.start_fall()

        ####
        ####

        self.sp.set_frame(self.states)
        self.sp.update()

####------------------------------------

    def draw(self):
        self.sp.draw()
        
####====================================
####
#### RUN

    def run_horizontal(self,dir):
        self.states = RUN_MASK | dir

####------------------------------------

    def stop_horizontal_move(self):
        if self.is_freefall:
            self.start_fall()
        elif self.is_falling():
            self.sp.dx = 0
            if self.can_stand():
                self.stop_fall()    
        else:
            self.states = STOP_MASK | self.get_direction()

####====================================
####
#### FALL

    def is_freefall(self):
        """落下開始にするかどうか"""
        if (
            self.check_ladder_top() or 
            self.check_ladder_btm() or
            self.check_ladder_belwo_btm() or
            self.can_stand()
            ):
            return(False)   # 梯子や床の上なら、落ちない
        else:
            return(True)    # そうでなければ落ちる

####------------------------------------

    def start_fall(self):
        self.states = FALL_MASK | self.get_direction()

####------------------------------------

    def stop_fall(self):
        if pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.KEY_D):
            self.states = RUN_MASK | self.get_direction(_)
        else:
            self.states = STOP_MASK | self.get_direction()

####====================================
####
#### LADDER
    
    def check_ladder_top(self):  # 頭正中2ドットが梯子か？
        x1,y1 = plus_tuple(self.sp.x,self.sp.y,TOP_CENTER1)
        x2,y2 = plus_tuple(self.sp.x,self.sp.y,TOP_CENTER2)
        if tl.is_ladder(x1,y1) and tl.is_ladder(x2,y2):
            return(True)
        else:
            return(False)
        
    def check_ladder_btm(self):  # 足元正中2ドットが梯子か？
        x1,y1 = plus_tuple(self.sp.x,self.sp.y,BTM_CENTER1)
        x2,y2 = plus_tuple(self.sp.x,self.sp.y,BTM_CENTER2)
        if tl.is_ladder(x1,y1) and tl.is_ladder(x2,y2):
            return(True)
        else:
            return(False)
        
    def check_ladder_below_btm(self):  # 足元正中の下の2ドットが梯子か？
        x1,y1 = plus_tuple(self.sp.x,self.sp.y,BTM_CENTER1)
        y1 += 1
        x2,y2 = plus_tuple(self.sp.x,self.sp.y,BTM_CENTER2)
        y2 += 1
        if tl.is_ladder(x1,y1) and tl.is_ladder(x2,y2):
            return(True)
        else:
            return(False)

####------------------------------------

    def check_ladder_up(self):
        """上移動可能ならTrue, できなければFalse"""
        if self.states == LAD_UP:
            if self.check_4corner_space() and self.can_stand():
                return(False)
        if self.check_ladder_top() or self.check_ladder_btm():
            return(True)
        else:
            return(False)

    def check_ladder_down(self):
        """下移動可能ならTrue, できなければFalse"""
        if (self.check_ladder_top() or
            self.check_ladder_btm() or
            self.check_ladder_below_btm()):
            return(True)
        else:
            return(False)

####------------------------------------

    def move_ladder(self,dir):
        
        # 上移動が可能なら登る
        if (
            (dir == UP) and
            (self.check_ladder_up()) and 
            not(self.check_bonk_head())
            ):
            self.states = LAD_UP
        
        # 下移動が可能なら下る
        elif (
            (dir == DOWN) and
            (self.check_ladder_down()) and
            not(self.check_on_the_wall())
            ):
            self.states = LAD_DN

####------------------------------------

    def stop_vertical_move(self):
        self.sp.dy = 0
        self.states = STOP_MASK | self.get_direction()

####====================================
####
#### JUMP

####====================================
####
#### CHECK & SOME FUNCTIONs

    def is_freefall(self):
        """落下開始にするかどうか"""
        if (self.check_ladder_up() or
            self.check_ladder_down() or
            self.can_stand()):   #梯子に掴まっている・立っているなら、
            return(False)
        else:
            return(True)
    
    def can_stand(self):
        x1,y1 = plus_tuple(self.sp.x,self.sp.y,BTM_SIDE_L)
        x2,y2 = plus_tuple(self.sp.x,self.sp.y,BTM_SIDE_R)
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

    def check_bonk_head(self):
        """上方向が壁に当たるならTrue"""
        x1,y1 = plus_tuple(self.sp.x,self.sp.y,TOP_SIDE_L)
        x2,y2 = plus_tuple(self.sp.x,self.sp.y,TOP_SIDE_R)
        if tl.is_wall(x1,y1) or tl.is_wall(x2,y2):
            return(True)
        else:
            return(False)
        
    def check_on_the_wall(self):
        """下方向が壁に当たるならTrue"""
        x1,y1 = plus_tuple(self.sp.x,self.sp.y,BTM_SIDE_L)
        x2,y2 = plus_tuple(self.sp.x,self.sp.y,BTM_SIDE_R)
        if tl.is_wall(x1,y1) or tl.is_wall(x2,y2):
            return(True)
        else:
            return(False)
        
####====================================

    def check_4corner_wall(self): # JSAN スプライトの四隅のドットが壁ならば
        revert=False
        for i in (TOPLEFT,TOPRIGHT,BTMLEFT,BTMRIGHT):
            cx,cy = plus_tuple(self.sp.x,self.sp.y, i)
            if tl.is_wall(cx,cy):
                revert = True
        if revert:
            self.sp.revert_xy()

    def check_btm_corner_wall(self): # 下２隅のどちらかが壁なら1ドット位置ずらす
        revert = False
        for i in (BTMLEFT,BTMRIGHT):
            cx,cy = plus_tuple(self.sp.x,self.sp.y, i)
            if tl.is_wall(cx,cy):
                revert = True
        if revert:
            self.sp.y = -1

    def check_4corner_ladder(self):
        for i in (TOPLEFT,TOPRIGHT,BTMLEFT,BTMRIGHT):
            cx,cy = plus_tuple(self.sp.x,self.sp.y, i)
            if tl.is_ladder(cx,cy):
                return(True)
            else:
                return(False)
            
    def check_4corner_space(self):
        for i in (TOPLEFT,TOPRIGHT,BTMLEFT,BTMRIGHT):
            cx,cy = plus_tuple(self.sp.x,self.sp.y, i)
            if tl.is_space(cx,cy):
                return(True)
            else:
                return(False)

#### 現在のstatesは梯子の昇降中か？

    def on_ladder(self):
        return(is_mask_true(self.states,LAD_MASK))

#### 落下中か？

    def is_falling(self):
        return(is_mask_true(self.states, FALL_MASK))