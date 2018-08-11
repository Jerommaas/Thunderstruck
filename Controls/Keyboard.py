from direct.showbase.DirectObject import DirectObject

class Arrows(DirectObject):
    def __init__(self,ControlManager):
        self.CM = ControlManager
        self.LeftPressed = 0
        self.RightPressed = 0
        self.KeyBindings()

    def KeyBindings(self):
        self.accept('arrow_left',self.Left_press)
        self.accept('arrow_left-up',self.Left_rel)
        self.accept('arrow_right',self.Right_press)
        self.accept('arrow_right-up',self.Right_rel)

        self.accept('arrow_up',self.Up_press)
        self.accept('arrow_up-up',self.Up_rel)

        self.accept('arrow_down',self.Down_press)
        self.accept('arrow_down-up',self.Down_rel)

        # Remind:
        # self.Steer()
        # self.Throttle()
        # self.Brake()
        # are methods from superclass

        # Steering controls
    def Left_press(self):
        self.LeftPressed = 1
        self.LR_arrows()
    def Left_rel(self):
        self.LeftPressed = 0
        self.LR_arrows()
    def Right_press(self):
        self.RightPressed = 1
        self.LR_arrows()
    def Right_rel(self):
        self.RightPressed = 0
        self.LR_arrows()

    def LR_arrows(self):
        self.CM.Steer(self.RightPressed-self.LeftPressed)

        # Throttle controls
    def Up_press(self):
        self.CM.Throttle(1)
    def Up_rel(self):
        self.CM.Throttle(0)

        # Brake controls
    def Down_press(self):
        self.CM.Brake(1)
    def Down_rel(self):
        self.CM.Brake(0)

class WASD(Arrows):
    def KeyBindings(self):
        self.accept('a',self.Left_press)
        self.accept('a-up',self.Left_rel)
        self.accept('d',self.Right_press)
        self.accept('d-up',self.Right_rel)

        self.accept('w',self.Up_press)
        self.accept('w-up',self.Up_rel)

        self.accept('s',self.Down_press)
        self.accept('s-up',self.Down_rel)