import pyxel
import sprite.sprite as sp

####====================================

class Jsan:
    def __init__(self):
        self.sp = sp.AniSprite(125,30,0,0,60,"LT_STAND",sp.sp8Group)
        self.base = self.sp.y + self.sp.h
        self.sp.add_frame("LT_STADN",[0])
        self.sp.add_frame("LT_RUN",[1,2,3,2])
        self.sp.add_frmae("LT_JUMP",[8])
        self.sp.add_frame("RT_STAND",[4])
        self.sp.add_frame("RT_RUN",[5,6,7,6])
        self.sp.add_frame("RT_JUMP",[9])
    def update(self):
        pass
    def draw(self):
        pass

####====================================

class Game:
    def __init__(self):
        pyxel.init(256,256)
        pyxel.load("jumpsan.pyxres")
        self.js = Jsan()
        pyxel.run(self.update,self.draw)
        pass

    def update(self):
        self.js.update()

    def draw(self):
        pyxel.cls(0)
        self.js.draw()

if __name__=="__main__":
    Game()