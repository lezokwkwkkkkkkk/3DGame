from direct.showbase.ShowBase import ShowBase
import pickle

class Mapmanager(ShowBase):
    def __init__(self, render, loader, file):
        self.loader = loader
        self.render = render
        self.land = None
        self.file = 'my_map.dat'
        self.model = 'block.egg'
        self.texture = 'block.png'
        self.colors = [(0.2, 0.2, 0.35, 1), 
                       (1, 0, 0, 1),
                       (0, 0, 1, 1), 
                       (0.2, 0.2, 0, 1)]
        self.color = (0.2, 0.2, 0.35, 1)
        self.color2 = (1, 0, 0, 1)
        self.color3 = (0, 0, 1, 1)
        self.color4 = (0.2, 0.2, 0, 1)
        self.load_land(file)

    def clear(self):
        if self.land:
            self.land.remove_node()
        self.startNew()

    def isEmpty(self, pos):
        blocks = self.findBlocks(pos)
        if blocks:
            return False
        return True

    def findBlocks(self, pos):
        return self.land.findAllMatches('=at=' + str(pos))
    
    def findHighestEmpty(self, pos):
        x, y, z = pos
        z = 1
        while not self.isEmpty((x, y, z)):
            z += 1
        return (x, y, z)

    def load_land(self, file):
        self.clear()
        file = open(file)
        file = file.readlines()
        y = 0
        for string in file:
            x= 0
            string_list = string.split(' ')
            for z  in string_list:
                for z_cor in range(int(z)):
                    self.addBlock((x, y, z_cor), self.setColor(z_cor))
                x += 1
            y += 1

    def setColor(self, z_cor):
        length = len(self.colors)
        if z_cor > length - 1:
            return self.setColor(z_cor - length)
        return self.colors[z_cor]

    def addBlock(self, pos, color):
        self.block = self.loader.loadModel(self.model)
        texture = self.loader.loadTexture(self.texture)
        self.block.setTexture(texture)
        self.block.setColor(color)
        self.block.setPos(pos)
        self.block.reparentTo(self.land)
        self.block.setTag('at', str(pos))
    
    def delBlock(self, pos):
        blocks = self.findBlocks(pos)
        for block in blocks:
            block.removeNode()
    
    def buildBlock(self, pos):
        x, y, z = pos
        new = self.findHighestEmpty(pos)
        if new[2] <= z+1:
            self.addBlock(new)

    def delBlockFrom(self, pos):
        x, y, z = self.findHighestEmpty(pos)
        pos = x, y, z-1
        blocks = self.findBlocks(pos)
        for block in blocks:
            block.removeNode()

    def saveMap(self):
        blocks = self.land.getChildren()
        fout = open(self.file, 'wb')
        pickle.dump(len(blocks), fout)
        for block in blocks:
            x, y, z = block.getPos()
            pos = (int(x), int(y), int(z))
            pickle.dump(pos, fout)
    
    def loadMap(self):
        self.clear()
        fin = open(self.file, 'rb')
        file_contents=str(fin.read())
        list_of_records=file_contents.split('.')
        no_of_records=len(list_of_records)-1
        fin.seek(0)
        for _ in range(no_of_records):
            pos = pickle.load(fin)
            print(pos)
            self.addBlock(pos)

    def startNew(self):
        self.land = self.render.attachNewNode("Land")