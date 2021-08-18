import sys
import json
import os
os.environ['CUDA_VISIBLE_DEVICES']='1'

from configparser import ConfigParser
from glob import glob
import json
import random
import math
# Blender
import bpy
sys.path.append(os.path.abspath((os.path.dirname(__file__))))
import xiuminglib as xm

def read_ini(path):
    config = ConfigParser()
    with open(path, 'r') as h:
        config.read_file(h)
    return config

def main():
    # Open scene
    xm.blender.scene.open_blend('./test.blend')
    config=read_ini('config_pifu_single.ini')
    if not os.path.exists(config.get('DEFAULT', 'save_path')):
        os.makedirs(config.get('DEFAULT', 'save_path'))

    # model path
    child_models=os.listdir(config.get('DEFAULT','model_path'))
    child_models.sort()
    #
    # # rendered model
    # rendered_models=os.listdir(config.get('DEFAULT', 'save_path'))
    for model in child_models:

        # Loading models
        xm.blender.render.set_cycles(w=config.getint('DEFAULT','img_size'),h=config.getint('DEFAULT','img_size'))

        # loading obj
        obj_path = os.path.join(config.get('DEFAULT', 'model_path'),model, 'pifu.obj')
        bpy.ops.import_scene.obj(filepath=obj_path,
                                 axis_forward='-Z', axis_up='Y', filter_glob="*.obj;*.mtl")  # -Z, Y()

        xm.blender.render.set_cycles(w=config.getint('DEFAULT', 'img_size'),
                                     h=config.getint('DEFAULT', 'img_size'))

        # Remove existing cameras and lights, if any
        for o in bpy.data.objects:
            o.select = o.type in ('LAMP', 'CAMERA')
        bpy.ops.object.delete()
        bpy.context.scene.update()

        for o in bpy.data.objects:
            if o.type == 'MESH':
                o.select = True

        # loading cam and light
        with open(os.path.join(config.get('DEFAULT', 'camera_path'), 'pifu.json'), 'r') as h:
            cam = json.load(h)

        cam_obj = xm.blender.camera.add_camera(
            xyz=cam['position'], rot_vec_rad=cam['rotation'],
            name=cam['name'],proj_model=cam['projection'],ortho_scale=cam['ortho_scale'],
            sensor_width=cam['sensor_width'], sensor_height=cam['sensor_height'],
            clip_start=cam['clip_start'], clip_end=cam['clip_end'])

        xm.blender.light.add_light_env(env=config.get('DEFAULT', 'light_path'))

        xm.blender.render.easyset(n_samples=config.getint('DEFAULT','samples'), color_mode='RGB')
        bpy.context.scene.use_nodes = True

        # Saving Render results
        target_path = os.path.join(config.get('DEFAULT', 'save_path'),model)
        if not os.path.exists(target_path):
            os.makedirs(target_path)

        # print(target_path)

        xm.blender.render.render(os.path.join(target_path,'raytracing.png'))

        for o in bpy.data.objects:
            if o.type == 'MESH':
                o.select = True
        bpy.ops.object.delete()
        bpy.context.scene.update()

    # xm.blender.scene.save_blend('./blender.blend')

if __name__ == '__main__':
    main()
