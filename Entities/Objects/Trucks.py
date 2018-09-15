import numpy as np
from Tools import *

modelfolder = "Entities/Objects/Models/"

class Basic:
    eggname = modelfolder+"Truck01/truck_01.egg"
    #eggname = modelfolder+"Environment/pine_tree_01.egg"

    # Static Class Properties
    turnradius = 15 #[m]
    sideacc    = 10 #[m/s2] acceleration when steering max
    forwardacc = 10 #[m/s2] without air drag
    topspeed = 40 #[m/s]
    brakespeed = 1 #[s] from topspeed to full stop
    mass = 1000 #[kg]

    # World Properties
    rho = 1.225 #[kg/m3] air density
    gravity = 9.81 #[m/s2]

    def __init__(self, World):
        self.Model()
        self.StartLocation()
        self.TruckParams()
        self.RotationMatrices()
        World.Clock.UpdateMe(self)

    def Model(self):
        self.m = loader.loadModel(self.eggname)
        self.m.reparentTo(render)

    def StartLocation(self):
        self.m.setPos(0,0,20)
        self.m.setHpr(0,0,0)

    def TruckParams(self):
        # User input
        self.Steer = 0
        self.Throttle = 0
        self.Brake = 0

        # Forces
        self.Fengine = self.mass * self.forwardacc
        self.Fbrake = self.mass * self.topspeed/self.brakespeed

        # Aerodynamics
        # At top speed: Fengine = 1/2 rho v2 Cd
        self.Cd = self.Fengine * 2 / self.rho / (self.topspeed**2)

        # Velocity
        self.Vbody = np.array([0.,0.,0.]) #[m/s]
        self.Vworld = np.array([0.,0.,0.]) #[m/s]

    def RotationMatrices(self):
        # Use attitude to compute Euler Transformation Matrices
        self.Truck2World, self.World2Truck = EulerAngles.RotMatDeg(self.m.getH(), self.m.getP(), self.m.getR())

    def Update(self,dt):
        # Get Euler Rotation Matrices
        Truck2World, World2Truck = EulerAngles.RotMatDeg(self.m.getH(), self.m.getP(), self.m.getR())

        # Perform turning
        Yaw = self.m.getH()
        turnrate = self.Steer * 360/4 # Hardcoded turnrate for now
        newYaw = Yaw + turnrate*dt
        self.m.setH(newYaw)

        # Only horizontal driving now, foeck gravity and terrain!
        Fdrag = 0.5 * self.rho * self.Vbody[1]**2 * self.Cd
        frontacc = (self.Throttle*self.Fengine - self.Brake*self.Fbrake - Fdrag)/self.mass
        # New velocity
        self.Vbody[1] = self.Vbody[1]+frontacc*dt
        self.Vbody[1] = max(self.Vbody[1],0)
        
        # Change frame of reference
        self.Vworld = np.dot(self.Vbody,self.World2Truck)


        # Update Position
        p = self.m.getPos()
        newP = np.array(p) + self.Vworld * dt
        self.m.setX(newP[0])
        self.m.setY(newP[1])

        self.m.setZ(newP[2])

        # New Rotation Matrices
        self.RotationMatrices()
