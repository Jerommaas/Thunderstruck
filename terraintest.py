from panda3d.core import GeoMipTerrain
from direct.task import Task
from direct.showbase.ShowBase import ShowBase

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        terrain = GeoMipTerrain("mySimpleTerrain")
        terrain.setHeightfield("Maps/simple.jpg")
        terrain.getRoot().setSz(50)
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
        
        myTexture = loader.loadTexture("Maps/stars.png")
        myTexture = loader.loadTexture("Maps/simple.jpg")
        terrain.getRoot().setTexture(myTexture)
        terrain.generate()

        skysphere = loader.loadModel("SkySphere.bam")
        skysphere.setBin('background', 1)
        skysphere.setDepthWrite(0) 
        skysphere.reparentTo(render)

        # Add a task to keep the sky dome fixed to the camera
        def skysphereTask(task):
          skysphere.setPos(base.camera, 0, 0, 0)
          return task.cont
        taskMgr.add(skysphereTask, "SkySphere Task")
        
        # Add a task to keep updating the terrain
        def updateTask(task):
          terrain.update()
          return task.cont
        taskMgr.add(updateTask, "update")

        

app = MyApp()
app.run()