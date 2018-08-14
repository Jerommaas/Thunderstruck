
modelfolder = "Entities/Objects/Models/"
class Truck01:
    eggname = modelfolder+"Truck01/truck_01.egg"
    def __init__(self):
        self.m = loader.loadModel(self.eggname)
        self.m.reparentTo(render)
        self.m.setPos(0,0,10)
        self.m.setHpr(0,90,0)