import numpy as np
from direct.task import Task

class Camera:
    Dist2Truck = 35 #[m]
    Azimuth    = 8 #[deg] position of camera wrt truck
    def __init__(self,World):
        # Stiekem bestaat er al een world.camera object
        self.World = World

        # Reference to the controlled truck!
        # Of course, must be replaced by networkcommunication
        self.Truck = World.Truck1

        # Relative position wrt Truck
        self.ComputePosition()

    def ComputePosition(self):
        AzRad = np.deg2rad(self.Azimuth)
        self.Position = self.Dist2Truck * np.array([0, -np.cos(AzRad), np.sin(AzRad)])

    def Update(self):
        TruckPosition = np.array(self.Truck.m.getPos())
        CamDistance = np.dot(self.Position,self.Truck.World2Truck)
        CamPosition = TruckPosition + CamDistance

        self.World.camera.setPos(tuple(CamPosition))

        self.World.camera.setHpr(self.Truck.m.getH(), 0, 0)