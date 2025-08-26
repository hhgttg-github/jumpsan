
import pyxel
import sprite.sprite as sp
import tile as tl

####====================================
#### CONSTANT

JS_WIDTH  = 8
JS_HEIGHT = 8
JS_W_EDGE = 7

# STATES

LEFT = 0b0000
RIGHT = 0b0001

STOP = 0b0000
RUN  = 0b0010
JUMP = 0b0100
FALL = 0b0110

JUMPABLE = [STOP,RUN]

HRZ_MOVE = 1024 # HORIZONTAL MOVE 横方向移動量

FALL_Y_MAX = 512       #落下の最高速度　これ以上は加速しない

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

####------------------------------------

    def stop_move(self):
        self.states = STOP

####------------------------------------

    def run_horizontal(self,dir):
        self.direction = dir
        self.states = RUN
    
####------------------------------------

    def move_horizontal(self,dir):
        self.sp.set_frame(self.states + dir)

####------------------------------------

    def start_falling(self):
        self.states = FALL
        self.sp.dy = FALL_Y_MAX
        self.sp.dx = 0

####------------------------------------

    def falling(self):
        self.states = FALL

####------------------------------------

    def update(self):

        if not(self.can_stand()): #立っていられない場所なら
            self.start_falling()
        else:
            self.stop_move()

        if pyxel.btnp(pyxel.KEY_SPACE) and (self.state in JUMPABLE):
                self.start_jump()

        if pyxel.btn(pyxel.KEY_A):
            self.run_horizontal(LEFT)
        elif pyxel.btn(pyxel.KEY_D):
            self.run_horizontal(RIGHT)
        elif (pyxel.btnr(pyxel.KEY_A)) or (pyxel.btnr(pyxel.KEY_D)):
            self.stop_move()

        self.sp.set_frame(self.states + self.direction)    
        self.sp.update()

####------------------------------------

    def draw(self):
        self.sp.draw()
        
####====================================

    def can_stand(self):
        xx = self.sp.x + JS_W_EDGE
        yy = self.sp.y + JS_HEIGHT
        if (tl.can_stand(self.sp.x,yy)) or (tl.can_stand(xx,yy)):
            return(True)
        else:
            return(False)