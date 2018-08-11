from panda3d.core import Texture, TextureStage, DirectionalLight, AmbientLight, TexGenAttrib, VBase4
from panda3d.core import ColorBlendAttrib, LPoint3, LVector4
from direct.filter.CommonFilters import CommonFilters
from panda3d.core import PandaNode, NodePath
import sys
import os

def Build():
    ##-- load a skydome from a bam file --##
    # this skydome is a small inverted sphere (inverted = back culling makes it transparent outside-in instead of inside-out)
    # that is wrapped around the camera (you can see what's happening by turning on base.oobe(), with togles out of body experience mode)
    # the camera is set as parent, such that the dome will stay centered around the camera.
    # compass makes sure that rotations of the camera are ignored, allowing you to look around the skydome.
    # the sphere is kept small, but disabling depth buffer and ensuring it is the first thing added to the render buffer alllows us to create the illusion that it is infinitely far away.
    # note: SkySphere.bam has to be be re-created for each Panda3D version. you can do so by running sky Sphere.py

    # load inverted sphere model, to texture
    skybox = loader.loadModel("Entities/Maps/skydome1/InvertedSphere.egg")
    # create 3D texture coordinates on sphere
    skybox.setTexGen(TextureStage.getDefault(), TexGenAttrib.MWorldPosition)
    skybox.setTexProjector(TextureStage.getDefault(), render, skybox)
    #skybox.setTexGen(TextureStage.getDefault(), TexGenAttrib.MWorldPosition)
    #skybox.setTexProjector(TextureStage.getDefault(), render, skybox)

    # create a cube map texture from 6 separate textures: (# should run 0-5)
    tex = loader.loadCubeMap('Entities/Maps/skydome1/lakes_#.png')
    tex2 = loader.loadCubeMap('Entities/Maps/skydome1/lakes_#_bloom.png')
    ts = TextureStage('ts')
    skybox.setTexGen(ts, TexGenAttrib.MWorldPosition)
    skybox.setTexProjector(ts, render, skybox)
    ts.setMode(TextureStage.MModulateGlow)
    # and give it to inverted sphere
    #skybox.setTexture(TextureStage.getDefault(),tex)
    skybox.setTexture(ts,tex)

    #TODO: make sure that this cube map and .eeg model are loaded from a BAM file for faster loading. (and don't forget to re-set textProjector after loading!)
    # load model (sphere + texture)
    #skybox = loader.loadModel("SkySphere.bam")
    # tell renderer how to project the texture to this sphere
    #skybox.setTexProjector(TextureStage.getDefault(), render, skybox) 

    # origen of model is on the surface. Let's move to the centre 
    # (and make it a little larger to prevent it from intersecting the camera's fustrum)
    skybox.setPos(0,0.5,0)
    skybox.setScale(2)
    # and slave it to the camera
    skybox.wrtReparentTo(camera) # note: cam vs. camera! (cam will make skydome look normal even in oobe mode)
    # altough parented by camera, tell to ignore camera rotations:
    skybox.setCompass()
    # tell renderer to use it as background (i.e. first to be rendered), and exclude it from depth buffer
    skybox.set_bin("background", 0)
    skybox.set_depth_write(0)
    # ignore light effects?
    skybox.setLightOff()


    render.setShaderAuto()
    filters = CommonFilters(base.win, base.cam)
    filterok = filters.setBloom(blend=(0, 0, 0, 1), desat=-0.5, mintrigger =0.1, intensity=-8.0, size="medium")

    # ass some light
    
    dlight = DirectionalLight('dlight')
    alight = AmbientLight('alight')
    dlnp = render.attachNewNode(dlight)
    alnp = render.attachNewNode(alight)
    dlight.setColor((0.2, 0.7, 0.2, 1))
    alight.setColor((0.2, 0.2, 0.2, 1))
    dlnp.setHpr(0, -60, 0)
    render.setLight(dlnp)
    render.setLight(alnp)
   





    #base.oobe()