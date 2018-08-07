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

        self.skysphere = self.loader.loadModel("SkySphere.bam")
        #self.skysphere.setBin('background', 1)
        self.skysphere.setDepthWrite(0) 
        self.skysphere.reparentTo(render)
        self.taskMgr.add(self.skysphereTask, "SkySphere Task")

        
        
        
        # Add a task to keep updating the terrain
        def updateTask(task):
          terrain.update()
          return task.cont
        taskMgr.add(updateTask, "update")

    # Add a task to keep the sky dome fixed to the camera
    def skysphereTask(self,task):
      self.skysphere.setPos(self.cam.getPos())
      #setpoc(base.cam,0,0,0) differs from setPos(base.cam.getPos()). latter stays at texture origen
      return task.cont

        

app = MyApp()
app.run()