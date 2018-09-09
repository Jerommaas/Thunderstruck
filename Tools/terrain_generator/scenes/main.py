
import gui
import panda_window
import data_object

from panda3d.core import *

loadPrcFileData("", "window-type none")

from direct.showbase.ShowBase import ShowBase

from direct.showbase.DirectObject import DirectObject
from panda3d.core import WindowProperties

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import sys

getModelPath().appendDirectory('/c/Panda3D-1.9.4-x64/models/') 


P3D_WIN_WIDTH = 400
P3D_WIN_HEIGHT = 240

class QTPandaWidget(QWidget):
	def __init__(self, parent=None):
		super(QWidget, self).__init__(parent)
		self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
		
	def resizeEvent(self, evt):
		wp = WindowProperties()
		wp.setSize(self.width(), self.height())
		wp.setOrigin(self.x(),self.y())
		base.win.requestProperties(wp)
	
	def minimumSizeHint(self):
		return QSize(400,300)

class QTTest(QDialog):
    def __init__(self, pandaCallback, parent=None):
        super(QDialog, self).__init__(parent)
        self.setWindowTitle("Test")
        self.setGeometry(0,0,400,300)
        
        self.pandaContainer = QTPandaWidget(self)
        # self.pandaContainer = QWidget(self)
        self.pandaContainer.setGeometry(0,0,P3D_WIN_WIDTH,P3D_WIN_HEIGHT)

        self.lineedit = QLineEdit("Write something...does it work?")
        
        layout = QVBoxLayout()
        layout.addWidget(self.pandaContainer)
        layout.addWidget(self.lineedit)
        
        self.setLayout(layout)
        
        # this basically creates an idle task
        self.timer =  QTimer(self)
        self.timer.timeout.connect( pandaCallback )
        self.timer.start(1)

    

    
class World(ShowBase):   
    def __init__(self):
        ShowBase.__init__(self)
        self.accept("a", self.pressedA)
        self.accept("escape", sys.exit)
        
    
    def pressedA(self):
        print( "a pressed, keyboard focus ok")
        # Load the environment model.
        self.scene = loader.loadModel("environment")
        # Reparent the model to render.
        self.scene.reparentTo(self.render)
        # Apply scale and position transforms on the model.
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-8, 42, 0)
        
    def step(self):
        taskMgr.step()
    
    def bindToWindow(self, windowHandle):
        wp = WindowProperties().getDefault()
        wp.setOrigin(0,0)
        wp.setSize(P3D_WIN_WIDTH, P3D_WIN_HEIGHT)
        wp.setParentWindow(windowHandle)
        base.openDefaultWindow(props=wp )
        self.wp = wp
        
    
if __name__ == '__main__':
    world = World()

    app = QApplication(sys.argv)
    form = QTTest(world.step)
    world.bindToWindow(int(form.winId()))
    
    form.show()
    app.exec_()