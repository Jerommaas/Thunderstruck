#import direct.directbase.DirectStart
from panda3d.core import GeoMipTerrain
from panda3d.core import Vec3
from panda3d.core import Texture, TextureStage, DirectionalLight, AmbientLight, TexGenAttrib, VBase4
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


        ##-- load a skydome from a bam file --##
        # this skydome is a small inverted sphere (inverted = back culling makes it transparent outside-in instead of inside-out)
        # that is wrapped around the camera (you can see what's happening by turning on base.oobe(), with togles out of body experience mode)
        # the camera is set as parent, such that the dome will stay centered around the camera.
        # compass makes sure that rotations of the camera are ignored, allowing you to look around the skydome.
        # the sphere is kept small, but disabling depth buffer and ensuring it is the first thing added to the render buffer alllows us to create the illusion that it is infinitely far away.
        # note: SkySphere.bam has to be be re-created for each Panda3D version. you can do so by running sky Sphere.py

        # load model (sphere + texture)
        self.skybox = self.loader.loadModel("SkySphere.bam")
        # tell renderer how to project the texture to this sphere
        self.skybox.setTexProjector(TextureStage.getDefault(), render, self.skybox) 

        # origen of model is on the surface. Let's move to the centre 
        # (and make it a little larger to prevent it from intersecting the camera's fustrum)
        self.skybox.setPos(0,0.5,0)
        self.skybox.setScale(2)
        # and slave it to the camera
        self.skybox.wrtReparentTo(self.camera) # note: cam vs. camera! (cam will make skydome look normal even in oobe mode)
        # altough parented by camera, tell to ignore camera rotations:
        self.skybox.setCompass()
        # tell renderer to use it as background (i.e. first to be rendered), and exclude it from depth buffer
        self.skybox.set_bin("background", 0)
        self.skybox.set_depth_write(0)
        # ignore light effects?
        self.skybox.setLightOff()
        
        
        #base.oobe()


        
        
        
        # Add a task to keep updating the terrain
        def updateTask(task):
          terrain.update()
          return task.cont
        taskMgr.add(updateTask, "update")

        

app = MyApp()
app.run()