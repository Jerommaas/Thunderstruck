from panda3d.core import GeoMipTerrain, Texture, TextureStage,SamplerState
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
        self.terrain.setHeightfield("Entities/Maps/heightmap.png")
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

        # some tinkering
        """
        # tell renderer to repeat texture when reading over the edge.
        texGrass.setWrapU(Texture.WM_repeat)
        texGrass.setWrapV(Texture.WM_repeat)
        # apply mipmapping: tell renderer how to handle multiple texture pixels being rendered t a single screen pixel (makes textures 30% larger in GPU mem.)
        texGrass.setMinfilter(SamplerState.FT_linear_mipmap_linear)
        """
        self.terrain.generate()
        




        """
        new attempt to include blend mapping:
        """
        # determine terrain size
        self.heightmap = self.terrain.heightfield()
        if self.heightmap.getXSize() > self.heightmap.getYSize():
            self.size = self.heightmap.getXSize()-1
        else:
            self.size = self.heightmap.getYSize()-1
        self.xsize = self.heightmap.getXSize()-1
        self.ysize = self.heightmap.getYSize()-1

        # Set multi texture
        # Source http://www.panda3d.org/phpbb2/viewtopic.php?t=4536
        self.generateSurfaceTextures()
        
     
        # load a blend texture from file:
        self.blendTexture = loader.loadTexture("Entities/Maps/blendMap.png")
        
        self.blendTS = TextureStage('blend')
        self.blendTS.setSort(0)
        self.blendTS.setPriority(1)
        # apply textures to the terrain and connect custom shader for blend mapping:
        self.setSurfaceTextures() 







        # Add a task to keep updating the terrain (for changing terrain, or synamic resolution)
        def updateTask(task):
            self.terrain.update()
            return task.cont
        taskMgr.add(updateTask, "update")

        # this is where we load the textures to be assigned to the terrain
    def generateSurfaceTextures(self):
        # Textureize
        self.grassTexture = loader.loadTexture("Entities/Maps/grassy2.png")
        self.grassTexture.setWrapU(Texture.WMRepeat)
        self.grassTexture.setWrapV(Texture.WMRepeat)
        self.grassTexture.setMinfilter(SamplerState.FT_linear_mipmap_linear)
        self.grassTexture.setAnisotropicDegree(8)
        self.grassTS = TextureStage('grass')
        self.grassTS.setSort(1) # sorting order is relevent for assigning textures to the four 
        
        self.rockTexture = loader.loadTexture("Entities/Maps/simple.jpg")
        self.rockTexture.setWrapU(Texture.WMRepeat)
        self.rockTexture.setWrapV(Texture.WMRepeat)
        self.rockTexture.setMinfilter(SamplerState.FT_linear_mipmap_linear)
        #self.grassTexture.setAnisotropicDegree(8)
        self.rockTS = TextureStage('rock')
        self.rockTS.setSort(2)
        # self.rockTS.setCombineRgb(TextureStage.CMAdd, TextureStage.CSLastSavedResult, TextureStage.COSrcColor, TextureStage.CSTexture, TextureStage.COSrcColor)
        
        self.sandTexture = loader.loadTexture("Entities/Maps/stars.png")
        self.sandTexture.setWrapU(Texture.WMRepeat)
        self.sandTexture.setWrapV(Texture.WMRepeat)
        self.sandTexture.setMinfilter(SamplerState.FT_linear_mipmap_linear)
        #self.sandTexture.setAnisotropicDegree(8)
        self.sandTS = TextureStage('sand')
        self.sandTS.setSort(3)
        self.sandTS.setPriority(5) # TODO: figure out what this is for...
        
        self.snowTexture = loader.loadTexture("Entities/Maps/grass.png")
        self.snowTexture.setWrapU(Texture.WMRepeat)
        self.snowTexture.setWrapV(Texture.WMRepeat)
        self.snowTexture.setMinfilter(SamplerState.FT_linear_mipmap_linear)
        #self.snowTexture.setAnisotropicDegree(8)
        self.snowTS = TextureStage('snow')
        self.snowTS.setSort(4)
        self.snowTS.setPriority(0)
        
        # a background (or rather freground?) texture that will be present independently from the blend map (consider removal)
        self.overlayTexture = loader.loadTexture("Entities/Maps/heightmap.png")
        self.overlayTexture.setWrapU(Texture.WMRepeat)
        self.overlayTexture.setWrapV(Texture.WMRepeat)
        self.overlayTexture.setMinfilter(SamplerState.FT_linear_mipmap_linear)
        #self.overlayTexture.setAnisotropicDegree(8)
        self.overlayTS = TextureStage('overlay')
        self.overlayTS.setSort(5)
        self.overlayTS.setPriority(10)



    # this is where we assign loaded textures to be blended in the shader.    
    def setSurfaceTextures(self):
        self.ownerview = False
        root = self.terrain.getRoot()
        root.clearTexture()
        #self.terrain.setTextureMap()
        root.setTexture( self.blendTS, self.snowTexture ) # this texture determines where the other textures are visible

        root.setTexture( self.grassTS, self.snowTexture )
        #root.setTexScale(self.grassTS, self.size*5, self.size*5) # I try to make the texture 20 times smaller then the blend map...

        root.setTexture( self.rockTS, self.snowTexture ) #rockTexture
        #root.setTexScale(self.rockTS, self.size*5, self.size*5) 

        root.setTexture( self.sandTS, self.snowTexture) #sandTexture
        #root.setTexScale(self.sandTS, self.size*5, self.size*5) 

        root.setTexture( self.snowTS, self.snowTexture ) #snowTexture
        #root.setTexScale(self.snowTS, self.size*5, self.size*5) 

        #(consider removal)
        root.setTexture( self.overlayTS, self.overlayTexture ) #overlayTexture
        #root.setTexScale(self.overlayTS, self.xsize, self.ysize)

        root.setShaderInput('size', self.xsize, self.ysize, self.size, self.size)
        root.setShader(loader.loadShader('Entities/Maps/terrainblender.sha'))