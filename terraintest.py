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


        #"""
        ##-- create a skydome from scratch --##
        # this setup creates a unit inverted globe, textures the inside with a cubeMap and centers it.
        # it 
        self.skybox = loader.loadModel("Maps/skydome1/InvertedSphere.egg")
        # create 3D texture coordinates on sphere
        self.skybox.setTexGen(TextureStage.getDefault(), TexGenAttrib.MWorldPosition)
        self.skybox.setTexProjector(TextureStage.getDefault(), render, self.skybox)
        self.skybox.setTexPos(TextureStage.getDefault(), 0, 0, 0)
        self.skybox.setTexScale(TextureStage.getDefault(), .5)
        # load a cube map texture: (# should run 0-5)
        tex = loader.loadCubeMap('Maps/skydome1/lakes_#.png')
        # and give it to inverted sphere
        self.skybox.setTexture(tex)
        #"""


        ##-- (option 2: not working?!) load a skydome from a bam file --##
        # SkySphere.bam can be created by running skySphere.py
        #self.skybox = self.loader.loadModel("SkySphere.bam")



        # origen of model is on the surface. Let's move to the centre 
        # (and make it a little larger to permit for difference between cam and camera)
        self.skybox.setPos(0,0.5,0)
        self.skybox.setScale(2)
        # altough parented by camera, tell to ignore camera rotations:
        self.skybox.setCompass()
        # tell renderer to use it as background, and exclude it from depth buffer
        self.skybox.set_bin("background", 0)
        self.skybox.set_depth_write(0)
        # ignore light effects?
        self.skybox.setLightOff()
        # and slave it to the camera
        self.skybox.wrtReparentTo(self.camera) # note: cam vs. camaera!
        
        #base.oobe()


        
        
        
        # Add a task to keep updating the terrain
        def updateTask(task):
          terrain.update()
          return task.cont
        taskMgr.add(updateTask, "update")

        

app = MyApp()
app.run()