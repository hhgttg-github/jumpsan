
import pyxel
import sprite.sprite as sp

####====================================
#### CONSTANT

# STATES

STOP_L = 0
STOP_R = 1
RUN_L  = 2
RUN_R  = 3
JUMP_L = 4
JUMP_R = 5
FALL_L = 6
FALL_R = 7

STOP  = [STOP_L,STOP_R]
RUN   = [RUN_L,RUN_R]
JUMP  = [JUMP_L,JUMP_R]
FALL  = [FALL_L,FALL_R]
LEFT  = [STOP_L,RUN_L,JUMP_L,FALL_L]
RIGHT = [STOP_R,RUN_R,JUMP_R,FALL_R]

JUMPABLE = [STOP_L,STOP_R,RUN_L,RUN_R]
JUMPING  = [JUMP_L,JUMP_R]

HRZ_MOVE = 1024 # HORIZONTAL MOVE 横方向移動量

STOP_JUMP_V = -3072     #停止からのジャンプ初速y
RUN_JUMP_V  = -4096     #走りながらのジャンプ初速y

JUMP_DY_3 = 128         #2000-のジャンプ速度のときの減速量dy
JUMP_DY_2 = 256         #1000-2000のときの減速量dy
JUMP_DY_1 = 512         #1000-のときの減速料dy

FALL_Y_1 = 512          #0-1000のときの落下加速度dy
FALL_Y_2 = 1024         #1000-2000のときの落下加速度dy
FALL_Y_MAX = 2048       #落下の最高速度　これ以上は加速しない

####====================================

class Jsan:

    def __init__(self):
        self.sp = sp.AniSprite(0,0,0,0,2,STOP_L,sp.sp8Group)
        self.base = self.sp.y + self.sp.h
        self.states = STOP_L
        self.vertical_speed = 0

        self.sp.add_frame(STOP_L,[0],0,(0,0))
        self.sp.add_frame(RUN_L, [1,2,3,2],3,(HRZ_MOVE*(-1),0))
        self.sp.add_frame(JUMP_L,[8],0,None)
        self.sp.add_frame(FALL_L,[8],0,None)
        self.sp.add_frame(STOP_R,[4],0,(0,0))
        self.sp.add_frame(RUN_R, [5,6,7,6],3,(HRZ_MOVE,0))
        self.sp.add_frame(JUMP_R,[9],0,None)
        self.sp.add_frame(FALL_R,[9],0,None)

####------------------------------------

    def run_horizontal(self,dir):
        pass
    
####------------------------------------

    def move_horizontal(self,dir):
        self.sp.set_frame(dir)

####------------------------------------
    
    def stop_move(self):
        if (self.sp.key == RUN_L) or (self.sp.key == JUMP_L):
            self.sp.set_frame(STOP_L)
        if (self.sp.key == RUN_R) or (self.sp.key == JUMP_R):
            self.sp.set_frame(STOP_R)

####------------------------------------

    def start_jump(self):
        if self.state in RUN:
            self.sp.dy = RUN_JUMP_V
        else:
            self.sp.dy = STOP_JUMP_V

        if self.state in LEFT:
            self.state = JUMP_L
        else:
            self.state = JUMP_R
        
            
####------------------------------------

    def keep_jump(self):
        pass

####------------------------------------

    def falling(self):
        if self.dy <= 1000:
            self.dy += FALL_Y_1
        elif self.dy <= 2000:
            self.dy += FALL_Y_2
        elif self.dy > FALL_Y_MAX:
            self.dy = FALL_Y_MAX

####------------------------------------

    def update(self):


        if self.state in [FALL_L,FALL_R]:
            if pyxel.btn(pyxel.KEY_A):
                self.sp.dx = HRZ_MOVE * (-1)
            elif pyxel.btn(pyxel.KEY_D):
                self.sp.dx = HRZ_MOVE
            self.falling()

        if pyxel.btnp(pyxel.KEY_SPACE) and (self.state in JUMPABLE):
                self.start_jump()
        
        if pyxel.btn(pyxel.KEY_SPACE) and (self.state in JUMPING):
            if pyxel.btn(pyxel.KEY_A):
                self.sp.dx = HRZ_MOVE * (-1)
            elif pyxel.btn(pyxel.KEY_D):
                self.sp.dx = HRZ_MOVE
            self.keep_jump()

        if pyxel.btn(pyxel.KEY_A):
            self.run_horizontal(LEFT)
        elif pyxel.btn(pyxel.KEY_D):
            self.run_horizontal(RIGHT)
        elif (pyxel.btnr(pyxel.KEY_A)) or (pyxel.btnr(pyxel.KEY_D)):
            self.stop_move()
        elif (pyxel.btnp(pyxel.KEY_SPACE)) and (self.state in JUMPABLE):
            self.start_jump()
        elif (pyxel.btn(pyxel.KEY_SPACE)) and (self.state in JUMPING):
            self.keep_jump()
        if (self.state==JUMP_L) or (self.state==JUMP_R):
            self.jumping()
        elif self.state == FALL:
            self.falling()
        self.sp.update()
        
    def draw(self):
        self.sp.draw()