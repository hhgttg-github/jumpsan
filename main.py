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
        self.sp = sp.AniSprite(0,0,0,0,2,STOP_L,sp.sp8Group)
        self.base = self.sp.y + self.sp.h
        self.sp.add_frame(STOP_L,[0],0,(0,0))
        self.sp.add_frame(RUN_L, [1,2,3,2],3,(-512,0))
        self.sp.add_frame(JUMP_L,[8],60,None)
        self.sp.add_frame(STOP_R,[4],0,(0,0))
        self.sp.add_frame(RUN_R, [5,6,7,6],3,(512,0))
        self.sp.add_frame(JUMP_R,[9],60,None)

    def run_horizontal(self,dir):
        self.sp.set_frame(dir)
    
    def stop_move(self):
        if (self.sp.key == RUN_L) or (self.sp.key == JUMP_L):
            self.sp.set_frame(STOP_L)
        if (self.sp.key == RUN_R) or (self.sp.key == JUMP_R):
            self.sp.set_frame(STOP_R)
        
    def update(self):
        if pyxel.btn(pyxel.KEY_A):
            self.run_horizontal(RUN_L)
        elif pyxel.btn(pyxel.KEY_D):
            self.run_horizontal(RUN_R)
        elif (pyxel.btnr(pyxel.KEY_A)) or (pyxel.btnr(pyxel.KEY_D)):
            self.stop_move()
        self.sp.update()
        
    def draw(self):
        self.sp.draw()

####====================================

class Game:
    def __init__(self):
        pyxel.init(128,128)
        pyxel.load("jumpsan.pyxres")
        self.js = Jsan()
        pyxel.run(self.update,self.draw)

    def update(self):
        self.js.update()

    def draw(self):
        pyxel.cls(0)
        pyxel.bltm(0,0,0,0,0,128,128)
        self.js.draw()

if __name__=="__main__":
    Game()   