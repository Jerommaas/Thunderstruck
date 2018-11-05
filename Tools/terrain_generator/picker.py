
#
# this class contains the picker node, which handles everything related to selecting 3d objects
#
#


class picker(object):
    def __init__(self, mouse, render, camera):
        self.mouse = mouse
        self.render = render 
        self.camera = camera
        # see:
        # http://www.panda3d.org/manual/index.php/Clicking_on_3D_Objects
        
        self.pickerNode = CollisionNode('mouseRay')
        pickerNP = camera.attachNewNode(self.pickerNode)
        self.pickerNode.setFromCollideMask(GeomNode.getDefaultCollideMask())
        self.pickerRay = CollisionRay()
        self.pickerNode.addSolid(self.pickerRay)
        self.traverser.addCollider(self.pickerNP, self.handle_picker() )

        
    def handle_picker(self):
        self.set_picker_ray()
        self.traverser.traverse(self.render)
        # Assume for simplicity's sake that myHandler is a CollisionHandlerQueue.
        if myHandler.getNumEntries() > 0:
            # This is so we get the closest object
            myHandler.sortEntries()
            pickedObj = myHandler.getEntry(0).getIntoNodePath()

    def set_picker_ray(self):
        # First we check that the mouse is not outside the screen.
        if not base.mouseWatcherNode.hasMouse():
            return

        mpos = base.mouseWatcherNode.getMouse()
        self.pickerRay.setFromLens(base.camNode, mpos.getX(), mpos.getY())


    