


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
    def __init__(self, parent, pandaWorld=None):   
        super(QWidget, self).__init__(parent)      
        self.pandaWorld = pandaWorld  
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
            print("save file as: {}".format(fileName) )
            self.pandaWorld.loader.save_scene(fileName)

    def loadDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Load File", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print("load file: {}".format(fileName) )
            print( self.pandaWorld )
            self.pandaWorld.loader.load_scene(fileName)

    def saveDialog(self): 
        # TODO: export options   
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, 'Export To ...',  "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            self.pandaWorld.loader.save_scene(fileName)
        
class tab_terrain(QWidget):
    '''
    Generation of terrain, including 
    - heightmaps, 
    - texture blending, 
    - skyboxes, skybox objects (distant buildings/mountains etc.)
    '''
    def __init__(self, parent, pandaWorld=None):   
        super(QWidget, self).__init__(parent)  
        self.layout = QVBoxLayout(self)
        label = QLabel(self)
        label.setText("Terrain tab")
        self.layout.addWidget(label)

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
    def __init__(self, parent, pandaWorld=None):   
        super(QWidget, self).__init__(parent) 
        self.layout = QVBoxLayout(self)
        self.pandaWorld = pandaWorld

        # tree 
        self.objectTreeView = QTreeView(self)

        # tree model
        self.treeview_model = QDirModel()   
        self.treeview_model.setFilter( QDir.NoSymLinks |  QDir.AllDirs | QDir.NoDotAndDotDot | QDir.Files | QDir.DirsFirst) 
        self.treeview_model.setNameFilters( ["*.egg"] ) 
        self.treeview_model.setSorting( QDir.Reversed)
        
        # TODO(victor): no hardcoded paths, get this at startup
        folder = "C:/Users/Victor/Desktop/thunderstruck/Thunderstruck/Entities/"
        print( "opening treeview in: {}".format(folder) )

        # 
        self.objectTreeView.setModel(self.treeview_model)
        self.objectTreeView.setColumnHidden(1, True)
        self.objectTreeView.setColumnHidden(2, True)
        self.objectTreeView.setColumnHidden(3, True) 
        self.objectTreeView.setRootIndex(self.treeview_model.index(folder))
        self.objectTreeView.setSortingEnabled(True) 
        self.objectTreeView.setAnimated(False) 
        self.objectTreeView.setSelectionMode(QAbstractItemView.SingleSelection)   
        self.objectTreeView.selectionModel().selectionChanged.connect(self.treeSelectionChange)

        # button
        qdir = QDir(path=folder) 
        self.pointlessButton = QPushButton(qdir.absolutePath()) 

        # label
        self.label = QLabel(self)
        self.label.setText("<file path>")

        # finalize
        self.layout.addWidget(self.pointlessButton)
        self.layout.addWidget(self.objectTreeView)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)
    
    def treeSelectionChange(self, index):  
        print("Selection changed:")
        for idx in self.objectTreeView.selectedIndexes():  
            indexItem = self.treeview_model.index(idx.row(), 0, idx.parent()) 
            fileName = self.treeview_model.fileName(indexItem)
            filePath = self.treeview_model.filePath(indexItem)
            print( "full path:\t{}\nfile: \t\t{}".format(filePath, fileName))
            self.label.setText(filePath) 
            # TODO(victor): detect if this is a file or a folder
            # TODO(victor): disable selecting folders




class tab_texture(QWidget):
    def __init__(self, parent, pandaWorld=None):   
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        label = QLabel(self)
        label.setText("Texture tab")
        self.layout.addWidget(label)


class tab_game_elements(QWidget):
    '''
    In this window, things like finish lines, invisible walls, event triggers, etc. can be edited
    '''
    def __init__(self, parent, pandaWorld=None):   
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.pandaWorld = pandaWorld
        label = QLabel(self)
        label.setText("Game elements tab")
        self.layout.addWidget(label)

class Gui(QWidget): 
    def __init__(self, parent, pandaWorld=None):   
        super(QWidget, self).__init__(parent)
        self.pandaWorld = pandaWorld

        self.layout = QVBoxLayout(self)
 
        # Initialize tab screen
        self.tabs = QTabWidget()

        self.tab_file = tab_file(self, pandaWorld=pandaWorld)	
        self.tab_terrain = tab_terrain(self, pandaWorld=pandaWorld)
        self.tab_object = tab_object(self, pandaWorld=pandaWorld)
        self.tab_game_elements = tab_game_elements(self, pandaWorld=pandaWorld) 
    
        self.tabs.resize(300,200) 
 
        # Add tabs
        self.tabs.addTab(self.tab_file,"File")
        self.tabs.addTab(self.tab_terrain,"Terrain")
        self.tabs.addTab(self.tab_object,"Objects")
        self.tabs.addTab(self.tab_game_elements, "Game elements") 
 
        # Add tabs to widget        
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)


if __name__ == "__main__":
    import main
    main.main()