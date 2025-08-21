import pyxel
import sprite.sprite as sp
from jsan import Jsan

####====================================
#### CONSTANT

####====================================
#### CLASS

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