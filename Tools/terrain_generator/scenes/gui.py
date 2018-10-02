


#
# This class contains the user interface.
# It also contains code to handle the panda frame
#

import os 
import sys

import main

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class tab_file(QWidget):
    '''
    Handles loading, saving(, exporting?) of the scene 
    '''
    def __init__(self, parent):   
        super(QWidget, self).__init__(parent)        
        self.layout = QVBoxLayout(self)

        # save button 
        self.saveButton = QPushButton("save button") 
        self.saveButton.clicked.connect(self.saveDialog)
        self.layout.addWidget(self.saveButton)

        # load button
        self.loadButton = QPushButton("load button") 
        self.loadButton.clicked.connect(self.loadDialog)
        self.layout.addWidget(self.loadButton)

        # Export button
        self.exportButton = QPushButton("export button") 
        #self.exportButton.clicked.connect(self.exportButton)
        self.layout.addWidget(self.exportButton)

        # layout
        self.setLayout(self.layout)

    def saveDialog(self):    
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName = QFileDialog.getSaveFileName(self, 'Save File',  "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print("save as: {}".format(fileName) )

    def loadDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Load File", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print("save as: {}".format(fileName) )

    def saveDialog(self): 
        # TODO: export options   
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName = QFileDialog.getSaveFileName(self, 'Export To ...',  "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print("save as: {}".format(fileName) )
        
class tab_terrain(QWidget):
    '''
    Generation of terrain, including 
    - heightmaps, 
    - texture blending, 
    - skyboxes, skybox objects (distant buildings/mountains etc.)
    '''
    def __init__(self, parent):   
        super(QWidget, self).__init__(parent)


def populateTree( tree, parent ):
    # TODO(victor): move to some util class
    for child in sorted(tree):
        child_item = QStandardItem(child)
        parent.appendRow(child_item)
        if isinstance(tree,dict):
            populateTree(tree[child], child_item)

        
class tab_object(QWidget):
    '''
    adding / editing / removing / animating objects
    '''
    def __init__(self, parent):   
        super(QWidget, self).__init__(parent) 
        self.layout = QVBoxLayout(self)

        # tree 
        self.objectTreeView = QTreeView(self)

        # tree model
        self.treeview_model = QDirModel()   
        self.treeview_model.setFilter( QDir.NoSymLinks |  QDir.AllDirs | QDir.NoDotAndDotDot | QDir.Files | QDir.DirsFirst) 
        self.treeview_model.setNameFilters( ["*.egg"] )
        
        self.treeview_model.setSorting( QDir.Reversed)
        
        folder = "C:/Users/Victor/Desktop/thunderstruck/Thunderstruck/Entities/"
        print( "opening treeview in: {}".format(folder) )

        #self.treeview_model.setRootPath(folder)
        self.objectTreeView.setModel(self.treeview_model)
        self.objectTreeView.setColumnHidden(1, True)
        self.objectTreeView.setColumnHidden(2, True)
        self.objectTreeView.setColumnHidden(3, True)
        
        self.objectTreeView.setRootIndex(self.treeview_model.index(folder))
        self.objectTreeView.setSortingEnabled(True)


        self.layout.addWidget(self.objectTreeView)

        # other
        qdir = QDir(path=folder) 
        self.pointlessButton = QPushButton(qdir.absolutePath()) 
        self.layout.addWidget(self.pointlessButton)

        # finalize
        self.setLayout(self.layout)

class tab_texture(QWidget):
    def __init__(self, parent):   
        super(QWidget, self).__init__(parent)

class tab_blend(QWidget):
    def __init__(self, parent):   
        super(QWidget, self).__init__(parent)

class tab_game_elements(QWidget):
    '''
    In this window, things like finish lines, invisible walls, event triggers, etc. can be edited
    '''
    def __init__(self, parent):   
        super(QWidget, self).__init__(parent)

class Gui(QWidget): 
    def __init__(self, parent):   
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
 
        # Initialize tab screen
        self.tabs = QTabWidget()

        self.tab_file = tab_file(self)	
        self.tab_terrain = tab_terrain(self)
        self.tab_object = tab_object(self)
        self.tab_game_elements = tab_game_elements(self)
        self.tab_export = tab_terrain(self) 
    
        self.tabs.resize(300,200) 
 
        # Add tabs
        self.tabs.addTab(self.tab_file,"File")
        self.tabs.addTab(self.tab_terrain,"Terrain")
        self.tabs.addTab(self.tab_object,"Objects")
        self.tabs.addTab(self.tab_game_elements, "Game elements")
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
    import main
    main.main()