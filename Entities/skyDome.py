from panda3d.core import Texture, TextureStage, DirectionalLight, AmbientLight, TexGenAttrib, VBase4
from panda3d.core import ColorBlendAttrib, LPoint3, LVector4
from direct.filter.CommonFilters import CommonFilters
from panda3d.core import PandaNode, NodePath
import sys
import os

class skyDome:
    def __init__(self):
        ##-- load a skydome from a bam file --##
        # this skydome is a small inverted sphere (inverted = back culling makes it transparent outside-in instead of inside-out)
        # that is wrapped around the camera (you can see what's happening by turning on base.oobe(), with togles out of body experience mode)
        # the camera is set as parent, such that the dome will stay centered around the camera.
        # compass makes sure that rotations of the camera are ignored, allowing you to look around the skydome.
        # the sphere is kept small, but disabling depth buffer and ensuring it is the first thing added to the render buffer alllows us to create the illusion that it is infinitely far away.
        # note: SkySphere.bam has to be be re-created for each Panda3D version. you can do so by running sky Sphere.py

        # load inverted sphere model, to texture
        #self.SkyDome = loader.loadModel("Entities/Maps/skydome1/InvertedSphere.egg")
        self.SkyDome = loader.loadModel("Entities/Maps/skydome1/spacedome.egg")
        # create 3D texture coordinates on sphere
        #self.SkyDome.setTexGen(TextureStage.getDefault(), TexGenAttrib.MWorldPosition) #* Copies the (x, y, z) position of each vertex, in world space, to the (u, v, w) texture coordinates.
        #self.SkyDome.setTexGen(TextureStage.getDefault(), TexGenAttrib.MEyePosition) # Copies the (x, y, z) position of each vertex, in camera space, to the (u, v, w) texture coordinates.
        #self.SkyDome.setTexGen(TextureStage.getDefault(), TexGenAttrib.MWorldNormal) # Copies the (x, y, z) lighting normal of each vertex, in world space, to the (u, v, w) texture coordinates.
        #self.SkyDome.setTexGen(TextureStage.getDefault(), TexGenAttrib.MEyeNormal) # Copies the (x, y, z) lighting normal of each vertex, in camera space, to the (u, v, w) texture coordinates.
        #self.SkyDome.setTexGen(TextureStage.getDefault(), TexGenAttrib.MEyeSphereMap) #* Generates (u, v) texture coordinates based on the lighting normal and the view vector to apply a standard reflection sphere map.
        #self.SkyDome.setTexGen(TextureStage.getDefault(), TexGenAttrib.MEyeCubeMap) # Generates (u, v, w) texture coordinates based on the lighting normal and the view vector to apply a standard reflection cube map.
        #self.SkyDome.setTexGen(TextureStage.getDefault(), TexGenAttrib.MWorldCubeMap) # Generates (u, v, w) texture coordinates based on the lighting normal and the view vector to apply a standard reflection cube map.



        #self.SkyDome.setTexProjector(TextureStage.getDefault(), render, self.SkyDome) # should only be needed when projectibf cube map to sphere...

        # create a cube map texture from 6 separate textures: (# should run 0-5)
        #tex = loader.loadCubeMap('Entities/Maps/skydome1/lakes_#.png')
        # or: get a pre-wrapped texture from the interwebs
        scene = loader.loadTexture('Entities/Maps/skydome1/14-Hamarikyu_Bridge_B_8k.jpg') #new
        

        #ts = TextureStage('ts')
        #self.SkyDome.setTexGen(ts, TexGenAttrib.MWorldPosition) # old
        #self.SkyDome.setTexGen(ts, TexGenAttrib.MEyeSphereMap) # new
        #self.SkyDome.setTexProjector(ts, render, self.SkyDome) # old
        # ts.setMode(TextureStage.MModulateGlow) # old

        # and give it to inverted sphere
        #self.SkyDome.setTexture(TextureStage.getDefault(),scene)
        #self.SkyDome.setTexture(ts,tex)

        #TODO: make sure that this cube map and .eeg model are loaded from a BAM file for faster loading. (and don't forget to re-set textProjector after loading!)
        # load model (sphere + texture)
        #self.SkyDome = loader.loadModel("SkySphere.bam")
        # tell renderer how to project the texture to this sphere
        #self.SkyDome.setTexProjector(TextureStage.getDefault(), render, self.SkyDome) 

        # origen of model is on the surface. Let's move to the centre 
        # (and make it a little larger to prevent it from intersecting the camera's fustrum)
        self.SkyDome.setPos(0,0.5,0)
        self.SkyDome.setScale(2)
        # and slave it to the camera
        self.SkyDome.wrtReparentTo(camera) # note: cam vs. camera! (cam will make skydome look normal even in oobe mode)
        # altough parented by camera, tell to ignore camera rotations:
        self.SkyDome.setCompass()
        # tell renderer to use it as background (i.e. first to be rendered), and exclude it from depth buffer
        self.SkyDome.set_bin("background", 0)
        self.SkyDome.set_depth_write(0)
        # ignore light effects?
        self.SkyDome.setLightOff()

        #base.oobe()
        #render.setShaderAuto()
        #filters = CommonFilters(base.win, base.cam)
        #filterok = filters.setBloom(blend=(0, 0, 0, 1), desat=-0.5, mintrigger =0.1, intensity=8.0, size="medium")

        # add some light
        
        dlight = DirectionalLight('dlight')
        alight = AmbientLight('alight')
        dlnp = render.attachNewNode(dlight)
        alnp = render.attachNewNode(alight)
        dlight.setColor((0.2, 0.2, 0.2, 1))
        alight.setColor((0.7, 0.7, 0.7, 1))
        dlnp.setHpr(60, -60, 0)
        render.setLight(dlnp)
        render.setLight(alnp)