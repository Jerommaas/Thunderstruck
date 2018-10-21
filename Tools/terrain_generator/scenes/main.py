 


import sys

# Panda
from panda3d.core import *  
loadPrcFileData("", "window-type none") 
from direct.showbase.DirectObject import DirectObject
from panda3d.core import WindowProperties

# QT
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# local
import gui
from pandaWorld import World

getModelPath().appendDirectory('/c/Panda3D-1.9.4-x64/models/') 



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

class QTMainWindow(QDialog):
    def __init__(self, pandaWorld=None, parent=None):
        super(QDialog, self).__init__(parent)
        self.setWindowTitle("Test")
        s = 80
        self.setGeometry(0,0,21*s,9*s)
        
        self.pandaContainer = QTPandaWidget(self) 
 
        layout = QHBoxLayout()
        layout.addWidget(self.pandaContainer) 
        user_interface = gui.Gui(self, pandaWorld=pandaWorld)
        layout.addWidget(user_interface)
        
        self.setLayout(layout) 
        self.pandaWorld = pandaWorld
        pandaWorld.bindToWindow(int(self.winId())) # window.pandaContainer.winId() or window.winId()? 
        # this basically creates an idle task
        # TODO(victor): run panda in separate thread if possible
        self.timer =  QTimer(self)
        self.timer.timeout.connect( pandaWorld.step )
        self.timer.start(0.01)



def main():
    pandaWorld = World()

    app = QApplication(sys.argv)
    window = QTMainWindow(pandaWorld=pandaWorld) 
    window.show()

    # ensure both qt and panda close
    sys.exit(app.exec_())
     
    
if __name__ == '__main__':
    main()