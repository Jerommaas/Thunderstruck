from panda3d.core import GeoMipTerrain
from direct.task import Task

class Terrain:
    def __init__(self):
        self.terrain = GeoMipTerrain("mySimpleTerrain")
        self.terrain.setHeightfield("Entities/Maps/simple.jpg")
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
        
        myTexture = loader.loadTexture("Entities/Maps/stars.png")
        myTexture = loader.loadTexture("Entities/Maps/simple.jpg")
        self.terrain.getRoot().setTexture(myTexture)
        self.terrain.generate()
        
        # Add a task to keep updating the terrain
        def updateTask(task):
            self.terrain.update()
            return task.cont
        taskMgr.add(updateTask, "update")