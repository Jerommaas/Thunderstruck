from direct.showbase.DirectObject import DirectObject
from direct.task import Task
import sys
from . import Keyboard
from . import Controller
#from . import xinput
from operator import attrgetter

class ControlManager(DirectObject):
    def __init__(self,World):
        self.accept('escape', sys.exit)

        # Reference to the controlled truck!
        # Of course, must be replaced by networkcommunication
        self.Truck = World.Truck1

        # Start different control inputs
        self.Arrows = Keyboard.Arrows(self)
        self.WASD = Keyboard.WASD(self)
        #self.SearchForControllers()

    def SearchForControllers(self):
        # Init the search for controllers
        def SearchTask(task):
            joys = xinput.XInputJoystick.enumerate_devices()
            if joys:
                # Joystick found: assume that it is X360
                self.X360 = Controller.X360(self,joys[0])
                return task.done
            else:
                task.delayTime = 3
                return task.again
        taskMgr.doMethodLater(0.1,SearchTask,'Search Controller')

        #########################################################
        # These functions must be replaced by handles to client comm
        #########################################################
    def Steer(self, value):
        # Set steering direction: [-1,1] [left, right]
        print("Steer", value)
        self.Truck.Steer = value

    def Throttle(self, value):
        # Set throttle: [0,1] [idle, full]
        print("Throttle", value*100,'%')
        self.Truck.Throttle = value

    def Brake(self, value):
        # Set Brake: [0,1] [none, full]
        print("Brake", value)
        self.Truck.Brake = value
        #########################################################