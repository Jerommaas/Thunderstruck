from direct.task import Task

FPS = 30
class WorldClock():
    def __init__(self):
        self.dt = 1/FPS
        self.dtcounter = 0
        # List of objects that have an Update(dt) function that needs to be called
        self.UpdateList = []

        # The task for our simulation
        def simulationTask(task):
            # Add the deltaTime for the task to the accumulator
            self.dtcounter += globalClock.getDt()
            while self.dtcounter > self.dt:
                # Remove a stepSize from the accumulator until
                # the accumulated time is less than the stepsize
                self.dtcounter -= self.dt
                # Step the simulation
                for Obj in self.UpdateList:
                    Obj.Update(self.dt)
            return task.cont

        taskMgr.doMethodLater(1.0, simulationTask, "Physics Simulation")

    def UpdateMe(self,Obj):
        # Add the Object to the list of appendables
        self.UpdateList.append(Obj)
