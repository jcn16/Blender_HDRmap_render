from ComputeCamParams import CamParams
import math
import json
import os

target_path='/media/jcn/新加卷/JCN/CLOTHES/Blender_rendering/metas/Oppo/cams'

default_dict={
    "clip_end": 100,
    "clip_start": 0.1,
    "focal_length": 22.63,
    "name": "P01",
    "position": [
        0,
        -1.4,
        0
    ],
    "projection": "perspective",
    "rotation": [
        1.57,
        0,
        0
    ],
    "sensor_fit": "horizontal",
    "sensor_height": 16,
    "sensor_width": 16
}

count=0
for r in [1.4,1.6,1.8]:
    for x_rad in range(-32,33,8):
        for z_rad in range(0,30,10):
            r=float(r)
            count+=1
            cam_position,cam_rotation=CamParams(r,x_rad,z_rad)

            default_dict["position"]=cam_position
            default_dict["rotation"]=cam_rotation
            default_dict["name"]=f'P{count}'

            dumps=json.dumps(default_dict,ensure_ascii=False, indent=4)

            cam_name=f'P{count}.json'
            with open(os.path.join(target_path,cam_name),'w') as f:
                f.write(dumps)


