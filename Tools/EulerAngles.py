import numpy as np
import math
# Calculates Rotation Matrix given euler angles
def RotMatDeg(z,y,x):
    return RotMat(np.deg2rad(z),np.deg2rad(y),np.deg2rad(x))
def RotMat(ang_z, ang_y, ang_x) :
    R_x = np.array([[1,         0,              0                 ],
                    [0,         math.cos(ang_x), -math.sin(ang_x) ],
                    [0,         math.sin(ang_x), math.cos(ang_x)  ]
                    ])
                  
    R_y = np.array([[math.cos(ang_y),    0,      math.sin(ang_y)  ],
                    [0,                  1,      0                ],
                    [-math.sin(ang_y),   0,      math.cos(ang_y)  ]
                    ])
                 
    R_z = np.array([[math.cos(ang_z),    -math.sin(ang_z),    0],
                    [math.sin(ang_z),    math.cos(ang_z),     0],
                    [0,                  0,                   1]
                    ])         
                     
    R = np.dot(R_z, np.dot( R_y, R_x ))
 
    return R, np.linalg.inv(R)