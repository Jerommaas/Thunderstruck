import numpy as np

modelfolder = "Entities/Objects/Models/"

class Basic:
    eggname = modelfolder+"Truck01/truck_01.egg"

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

    def Update(self,dt):
        # Perform turning
        Yaw = self.m.getH()
        turnrate = self.Steer * 360/4 # Hardcoded turnrate for now
        newYaw = Yaw + turnrate*dt
        self.m.setH(newYaw)

        # Only horizontal driving now, foeck gravity and terrain!
        frontacc = (self.Throttle*self.Fengine - self.Brake*self.Fbrake)/self.mass
        # New velocity
        self.Vbody[1] = self.Vbody[1]+frontacc*dt
        self.Vbody[1] = max(self.Vbody[1],0)

        # Forget rotation for now
        p = self.m.getPos()
        p[0] = p[0] + self.Vbody[1]*dt *-np.sin(np.deg2rad(newYaw))
        p[1] = p[1] + self.Vbody[1]*dt * np.cos(np.deg2rad(newYaw))
        self.m.setPos(p)