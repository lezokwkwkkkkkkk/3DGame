from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties
from mapmanager import Mapmanager
from hero import Hero

class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        properties = WindowProperties()
        properties.set_size(800, 600)
        self.win.requestProperties(properties)
        self.land = Mapmanager(self.render, self.loader, 'map.txt')
        self.hero = Hero((3, 3, 2), self.render, self.loader, self.land)
        self.camLens.setFov(90)

game = Game()
game.run()