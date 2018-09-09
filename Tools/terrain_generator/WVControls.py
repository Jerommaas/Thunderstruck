from direct.showbase.DirectObject import DirectObject
from direct.task import Task
import sys
from operator import attrgetter

class ControlManager(DirectObject):
    def __init__(self,World):
        self.accept('escape', sys.exit)
        self.W = 0
        self.A = 0
        self.S = 0
        self.D = 0
        self.Cam = World.Camera

        # Start different control inputs
        self.accept('a',self.A_press)
        self.accept('a-up',self.A_rel)
        self.accept('d',self.D_press)
        self.accept('d-up',self.D_rel)

        self.accept('w',self.W_press)
        self.accept('w-up',self.W_rel)
        self.accept('s',self.S_press)
        self.accept('s-up',self.S_rel)

    def A_press(self):
        self.A = 1
        self.Cam.AD = self.D - self.A
    def A_rel(self):
        self.A = 0
        self.Cam.AD = self.D - self.A

    def D_press(self):
        self.D = 1
        self.Cam.AD = self.D - self.A
    def D_rel(self):
        self.D = 0
        self.Cam.AD = self.D - self.A

    def W_press(self):
        self.W = 1
        self.Cam.WS = self.W - self.S
    def W_rel(self):
        self.W = 0
        self.Cam.WS = self.W - self.S

    def S_press(self):
        self.S = 1
        self.Cam.WS = self.W - self.S
    def S_rel(self):
        self.S = 0
        self.Cam.WS = self.W - self.S