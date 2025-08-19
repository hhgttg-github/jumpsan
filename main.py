import pyxel
import sprite.sprite as sp

####====================================
#### CONSTANT

STOP_L = 0
STOP_R = 1
RUN_L  = 2
RUN_R  = 3
JUMP_L = 4
JUMP_R = 5

####====================================

class Jsan:

    def __init__(self):
        self.sp = sp.AniSprite(125,30,0,0,2,STOP_L,sp.sp8Group)
        self.base = self.sp.y + self.sp.h
        self.sp.add_frame(STOP_L,[0])
        self.sp.add_frame(RUN_L, [1,2,3,2])
        self.sp.add_frame(JUMP_L,[8])
        self.sp.add_frame(STOP_R,[4])
        self.sp.add_frame(RUN_R, [5,6,7,6])
        self.sp.add_frame(JUMP_R,[9])

    def run_horizontal(self,dir):
        if dir == RUN_L:
            self.sp.key=RUN_L
            self.sp.speed(-512,0)
            self.sp.interval = 4
        elif dir == RUN_R:
            self.sp.key = RUN_R
            self.sp.speed(512,0)
            self.sp.intrvval = 4
    
    def stop_moving(self):
        if (self.sp.key == RUN_L) or (self.sp.key == JUMP_L):
            self.sp.key == STOP_L
            self.sp.dx = 0
            self.sp.interval = 60
            return()
        if (self.sp.key == RUN_R) or (self.sp.key == JUMP_R):
            self.sp.key == STOP_R
            self.sp.dx = 0
            self.sp.interval = 60
            return()
        
    def update(self):
        if pyxel.btn(pyxel.KEY_A):
            self.run_horizontal(RUN_L)
        elif pyxel.btn(pyxel.KEY_D):
            self.run_horizontal(RUN_R)
        else:
            self.stop_moving()
        self.sp.update()
        
    def draw(self):
        self.sp.draw()

####====================================

class Game:
    def __init__(self):
        pyxel.init(256,256)
        pyxel.load("jumpsan.pyxres")
        self.js = Jsan()
        pyxel.run(self.update,self.draw)

    def update(self):
        self.js.update()

    def draw(self):
        pyxel.cls(0)
        self.js.draw()

if __name__=="__main__":
    Game()   