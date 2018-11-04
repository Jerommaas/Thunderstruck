

import time 
import numpy as np

from direct.task import Task

import main

#
# Camera
#

class Camera(object):
    def __init__(self, world):
        self.world = world
        self.world.accept( "w", self.move_y, [1] )
        self.world.accept( "s", self.move_y, [-1])
        self.world.accept( "a", self.move_x, [-1] )
        self.world.accept( "d", self.move_x, [1] )

        self.world.accept( "w-up", self.move_y,[ 0])
        self.world.accept( "s-up", self.move_y, [0])
        self.world.accept( "a-up", self.move_x,  [0])
        self.world.accept( "d-up", self.move_x,  [0])

        self.time = time.time()
        self.pos = np.array( [0,0,1.8] )
        self.rot = np.array( [0,0,0] )

        self.control = np.array( [0,0] )

        # self.world.camera.node().getLens().setFov(120)

        # camera control
        taskMgr.add(self.tick, 'TickCameraMovement')

    def move_x(self, x):
        self.control[0] = x

    def move_y(self, y):
        self.control[1] = y


    def tick(self, task ):
        t_cur = time.time()
        dt = t_cur - self.time
        cam = self.world.camera

        vmax = 1

        yaw_deg = cam.get_h()
        pitch_deg = cam.get_p()
        roll_deg = cam.get_r()

        yaw = np.pi * yaw_deg  / 180
        pitch = np.pi * pitch_deg  / 180
        roll = np.pi * roll_deg  / 180

        # cam.set_p( t_cur )
        f = np.pi / 2
        forward = np.array( [np.cos(yaw), np.sin(yaw), 0 ]) # TODO(victor): calculate correct vectors
        right = np.array( [np.cos(yaw+f), np.sin(yaw+f), 0])
 
        self.pos = self.pos + (dt * self.control[0] * forward) # add forward movement
        self.pos = self.pos + (dt * self.control[1] * right) # add forward movement

        # cam.setPos( *self.pos ) 
        cam.set_x( self.pos[0] )
        cam.set_y( self.pos[1] )
        cam.set_z( self.pos[2] )
        
        # cam.set_p(  )
        cam.set_r( 0 )

        self.time = t_cur
        return task.cont


if __name__ == "__main__":
    main.main()