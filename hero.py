from direct.showbase.ShowBase import ShowBase
from mapmanager import Mapmanager

class Hero(ShowBase):
    land: Mapmanager
    def __init__(self, pos, render, loader, land):
        self.land = land
        self.render = render
        self.loader = loader
        self.mode = False
        self.hero = loader.loadModel('smiley')
        self.hero.setColor(1, 0.5, 0)
        self.hero.setScale(0.3)
        self.hero.setPos(pos)
        self.hero.reparentTo(render)
        self.accept_events()
        self.cameraBind()

    def move_to(self, angle):
        if self.mode:
            self.just_move(angle)
        else:
            self.try_move(angle)

    def look_at(self, angle):
        from_x = round(self.hero.getX())
        from_y = round(self.hero.getY())
        from_z = round(self.hero.getZ())
        dx, dy = self.check_dir(angle)
        return from_x + dx, from_y + dy, from_z

    def check_dir(self, angle):
        if angle >= 0 and angle <= 20:
           return (0, -1)
        elif angle <= 65:
           return (1, -1)
        elif angle <= 110:
            return (1, 0)
        elif angle <= 155:
            return (1, 1)
        elif angle <= 200:
            return (0, 1)
        elif angle <= 245:
            return (-1, 1)
        elif angle <= 290:
            return (-1, 0)
        elif angle <= 335:
            return (-1, -1)
        else:
            return (0, -1)
        
    def just_move(self, angle):
        pos = self.look_at(angle)
        self.hero.setPos(pos)
    
    def try_move(self, angle):
        pos = self.look_at(angle)
        if self.land.isEmpty(pos):
            pos = self.land.findHighestEmpty(pos)
            self.hero.setPos(pos)
        else:
            pos = pos[0], pos[1], pos[2] + 1
            if self.land.isEmpty(pos):
                self.hero.setPos(pos)


    def turn_left(self):
        self.hero.setH((self.hero.getH() +5) % 360)

    def turn_right(self):
        self.hero.setH((self.hero.getH() -5) % 360)

    def cameraBind(self):
        base.disable_mouse()
        base.camera.setH(180)
        base.camera.reparent_to(self.hero)
        base.camera.setPos(0, 3, 2)
        self.cameraOn = True

    def cameraUp(self):
        pos = self.hero.getPos()
        base.mouseInterfaceNode.setPos(-pos[0] - 1, -pos[1], -pos[2] - 3)
        base.camera.reparent_to(self.render)
        base.enable_mouse()
        self.cameraOn = False

    def back(self):
        angle = (self.hero.getH() + 180) % 360
        self.move_to(angle)
    
    def forward(self):
        angle = (self.hero.getH()) % 360
        self.move_to(angle)

    def left(self):
        angle = (self.hero.getH() + 90) % 360
        self.move_to(angle)

    def right(self):
        angle = (self.hero.getH() - 90) % 360
        self.move_to(angle)
    
    def up(self):
        self.hero.setZ(self.hero.getZ() + 1)

    def build(self):
        angle = self.hero.getH() % 360
        pos = self.look_at(angle)
        if not self.mode:
            self.land.addBlock(pos)
        else:
            self.land.buildBlock(pos)

    def destroy(self):
        angle = self.hero.getH() % 360
        pos = self.look_at(angle)
        if not self.mode:
            self.land.delBlock(pos)
        else:
            self.land.delBlockFrom(pos)

    def accept_events(self):
        base.accept('c', self.changeView)
        base.accept('a', self.turn_left)
        base.accept('a' + '-repeat', self.turn_left)
        base.accept('d', self.turn_right)
        base.accept('d' + '-repeat', self.turn_right)
        base.accept('arrow_down', self.back)
        base.accept('arrow_down' + '-repeat', self.back)
        base.accept('arrow_up', self.forward)
        base.accept('arrow_up' + '-repeat', self.forward)
        base.accept('arrow_left', self.left)
        base.accept('arrow_left' + '-repeat', self.left)
        base.accept('arrow_right', self.right)
        base.accept('arrow_right' + '-repeat', self.right)
        base.accept('space', self.up)
        base.accept('space' + '-repeat', self.up)
        base.accept('m', self.change_mode)
        base.accept('v', self.destroy)
        base.accept('b', self.build)
        base.accept('k', self.land.saveMap)
        base.accept('l', self.land.loadMap)

    def change_mode(self):
        self.mode = not self.mode
    
    def changeView(self):
        if self.cameraOn:
            self.cameraUp()
        else:
            self.cameraBind()

