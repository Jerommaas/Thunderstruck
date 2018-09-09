import numpy as np
from direct.task import Task

class Camera:
    movespeed = 40 #[m/s]
    FPS = 30
    def __init__(self,World):
        self.World = World
        self.Position = np.array([15,15,30])
        self.HPR = np.array([-20,0,0])
        self.WS = 0
        self.AD = 0

        self.dt = 1/self.FPS
        self.dtcounter = 0

        # The task for our simulation
        def simulationTask(task):
            # Add the deltaTime for the task to the accumulator
            dt = globalClock.getDt()
            self.World.Camera.Update(dt)
            return task.cont

        taskMgr.add(simulationTask, "Cam Movement")

    def Update(self,dt):
        print(self.World.camera.getH())
        rightvector = np.array([1,0,0])
        frontvector = np.array([0,1,0])
        self.Position = self.Position + rightvector * self.AD *self.movespeed*dt
        self.Position = self.Position + frontvector * self.WS *self.movespeed*dt
        self.World.camera.setPos(tuple(self.Position))
        self.World.camera.setHpr(tuple(self.HPR))