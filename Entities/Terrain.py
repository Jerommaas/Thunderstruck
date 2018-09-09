from panda3d.core import GeoMipTerrain
from panda3d.core import Filename
from direct.task import Task
import sys

import os
class Terrain:
    folder = os.path.dirname(os.path.abspath(__file__))
    subfolder = "/Maps/"
    file = "simple.jpg"
    filepath = folder+subfolder+file
    def __init__(self):
        fn = Filename.fromOsSpecific(self.filepath)
        self.terrain = GeoMipTerrain("mySimpleTerrain")
        self.terrain.setHeightfield(fn)
        self.terrain.getRoot().setSz(40)
        #terrain.setBruteforce(True)
        self.terrain.getRoot().reparentTo(render)

        # Set terrain properties
        self.terrain.setBlockSize(16)
        self.terrain.setNear(500)
        self.terrain.setFar(100)
        self.terrain.setFocalPoint(base.camera)
         
        # Store the root NodePath for convenience
        root = self.terrain.getRoot()
        root.reparentTo(render)

        myTexture = loader.loadTexture(fn)
        self.terrain.getRoot().setTexture(myTexture)
        self.terrain.generate()
        
        # Add a task to keep updating the terrain
        def updateTask(task):
            self.terrain.update()
            return task.cont
        taskMgr.add(updateTask, "update")