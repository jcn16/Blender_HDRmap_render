import numpy as np
import math

'''
coordinates

       z|
        |
        |
  cam  /----------y
      /
     /x 
        
'''
def CamParams(r,x_rad=0,z_rad=0):

    # Compute trans along y
    dx=r*np.cos(z_rad)*np.sin(x_rad)
    dy=r*np.cos(z_rad)*np.cos(x_rad)
    dz=r*np.sin(z_rad)

    cam_position=[dx,-dy,dz]
    cam_rotation=[-z_rad+math.pi/2,0,x_rad]

    return cam_position,cam_rotation



