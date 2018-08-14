from panda3d.core import GeoMipTerrain
from direct.task import Task

def Build():
    terrain = GeoMipTerrain("mySimpleTerrain")
    terrain.setHeightfield("Entities/Maps/simple.jpg")
    terrain.getRoot().setSz(40)
    #terrain.setBruteforce(True)
    terrain.getRoot().reparentTo(render)

    # Set terrain properties
    terrain.setBlockSize(16)
    terrain.setNear(500)
    terrain.setFar(100)
    terrain.setFocalPoint(base.camera)
     
    # Store the root NodePath for convenience
    root = terrain.getRoot()
    root.reparentTo(render)
    
    myTexture = loader.loadTexture("Entities/Maps/stars.png")
    myTexture = loader.loadTexture("Entities/Maps/simple.jpg")
    terrain.getRoot().setTexture(myTexture)
    terrain.generate()
    
    # Add a task to keep updating the terrain
    def updateTask(task):
        terrain.update()
        return task.cont
    taskMgr.add(updateTask, "update")