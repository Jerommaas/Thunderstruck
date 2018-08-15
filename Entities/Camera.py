import numpy as np
from direct.task import Task

class Camera:
    def __init__(self,World):
        # Stiekem bestaat er al een world.camera object
        self.World = World

        # Reference to the controlled truck!
        # Of course, must be replaced by networkcommunication
        self.Truck = World.Truck1

        taskMgr.add(self.FollowTruck, "Set Camera")

    def FollowTruck(self, task):
        angleDegrees = task.time * 25.0
        angleRadians = angleDegrees * (3.14 / 180.0)
        dist = 20*np.array([np.sin(angleRadians),np.cos(angleRadians),1/20])
        truckpos = np.array(self.Truck.m.getPos())
        campos = truckpos + dist
        print(truckpos,campos)

        self.World.camera.setPos(tuple(campos))

        self.World.camera.setHpr(angleDegrees, 0, 0)
        return Task.cont