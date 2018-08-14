
modelfolder = "Entities/Objects/Models/"

class Basic:
    eggname = modelfolder+"Truck01/truck_01.egg"

    # Static Class Properties
    turnradius = 15 #[m]
    acceleration = 10 #[m/s2] without air drag
    topspeed = 40 #[m/s]
    brakespeed = 1 #[s] from topspeed to full stop
    mass = 1000 #[kg]

    # World Properties
    rho = 1.225 #[kg/m3] air density
    gravity = 9.81 #[m/s2]

    def __init__(self):
        self.Model()
        self.StartLocation()
        self.TruckParams()

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
        self.Fengine = self.mass * self.acceleration
        self.Fbrake = self.mass * self.topspeed/self.brakespeed

        # Aerodynamics
        # At top speed: Fengine = 1/2 rho v2 Cd
        self.Cd = self.Fengine * 2 / self.rho / (self.topspeed**2)

        # Velocity
        self.V = (0,0,0) #[m/s]

    def Update(self,dt):
        # Only horizontal driving now, foeck gravity and terrain!
        pass