


#
# This class contains the user interface.
# It also contains code to handle the panda frame
#

import main

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class tab_file(QWidget):
    def __init__(self, parent):   
        super(QWidget, self).__init__(parent)
        
class tab_terrain(QWidget):
    def __init__(self, parent):   
        super(QWidget, self).__init__(parent)
        
class tab_object(QWidget):
    def __init__(self, parent):   
        super(QWidget, self).__init__(parent)

class tab_texture(QWidget):
    def __init__(self, parent):   
        super(QWidget, self).__init__(parent)

class tab_blend(QWidget):
    def __init__(self, parent):   
        super(QWidget, self).__init__(parent)

class tab_export(QWidget):
    def __init__(self, parent):   
        super(QWidget, self).__init__(parent)

class Gui(QWidget): 
    def __init__(self, parent):   
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
 
        # Initialize tab screen
        self.tabs = QTabWidget()

        self.tab_file = tab_file()	
        self.tab_terrain = tab_terrain()
        self.tab_object = tab_terrain()
        self.tab_export = tab_terrain() 
    
        self.tabs.resize(300,200) 
 
        # Add tabs
        self.tabs.addTab(self.tab_file,"File")
        self.tabs.addTab(self.tab_terrain,"Terrain")
        self.tabs.addTab(self.tab_object,"Objects")
        self.tabs.addTab(self.tab_export,"Export") 
 
        # # Create first tab
        # self.tab_file.layout = QVBoxLayout(self)
        # self.pushButton1 = QPushButton("PyQt5 button")
        # self.tab_file.layout.addWidget(self.pushButton1)
        # self.tab_file.setLayout(self.tab_file.layout)
 
        # Add tabs to widget        
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)


if __name__ == "__main__":
    gui = Gui(None)