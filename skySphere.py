import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from panda3d.core import Texture, TextureStage, DirectionalLight, AmbientLight, TexGenAttrib, VBase4

 
class SkySphere(DirectObject):
    def __init__(self):
        # load inverted sphere model, to texture
        self.sphere = loader.loadModel("Maps/skydome1/InvertedSphere.egg")
        # create 3D texture coordinates on sphere
        self.sphere.setTexGen(TextureStage.getDefault(), TexGenAttrib.MWorldPosition)
        self.sphere.setTexProjector(TextureStage.getDefault(), render, self.sphere)
        self.sphere.setTexPos(TextureStage.getDefault(), 0, 0, 0)
        self.sphere.setTexScale(TextureStage.getDefault(), .5)

        # load a cube map texture: (# should run 0-5)
        tex = loader.loadCubeMap('Maps/skydome1/lakes_#.png')
        # and give it to inverted sphere
        self.sphere.setTexture(tex)
        #We don't want't to do this all the time, so save it. BAM!
        result = self.sphere.writeBamFile("SkySphere.bam")
        print('skybox saved to BAM successully: '+str(result)) #print if we succeeded...

        self.sphere.set_bin("background", 0)
        self.sphere.setCompass()
        # ignore light ?
        self.sphere.setLightOff()
        # re-size sphere (1km diameter)
        
        self.sphere.setPos(0,0.5,0)
        self.sphere.setScale(2)
        

        # and render the sky box
        self.sphere.wrtReparentTo(camera)
        
        base.oobe()

SS = SkySphere()
run()