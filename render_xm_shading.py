import sys
import json
import os
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

def split_model_name(name):
    pitch=int(name.split('_')[0])
    yaw=int(name.split('_')[1])
    scale=float(name.split('_')[2])

    camera_length=len(str(pitch)+'_'+str(yaw)+'_'+str(scale)+'_')
    hdr=name[camera_length:-1]

    return pitch,yaw,scale,hdr


def main():
    # Open scene
    xm.blender.scene.open_blend('./test.blend')
    config=read_ini('./config.ini')
    if not os.path.exists(config.get('DEFAULT', 'save_path')):
        os.makedirs(config.get('DEFAULT', 'save_path'))

    # model path
    with open(os.path.join(config.get('DEFAULT', 'model_json_path'),'train.json'),'r') as f:
        child_models=json.load(f)
        child_models.sort()

    # HDR map path
    hdr_root_path='/media/jcn/新加卷/JCN/JCN_test_datset/HDR_Heaven/HDRI_8k'

    # Loading models
    for model in child_models:

        child_models=os.listdir(os.path.join(config.get('DEFAULT', 'root_path'),model))
        child_models.sort()

        xm.blender.render.set_cycles(w=config.getint('DEFAULT','img_size'),h=config.getint('DEFAULT','img_size'))

        # loading obj
        obj_path = os.path.join(config.get('DEFAULT', 'root_path'), model, model.split('-')[0] + '_scaled.obj')
        bpy.ops.import_scene.obj(filepath=obj_path,
                                 axis_forward='-Z', axis_up='Y', filter_glob="*.obj;*.mtl")  # -Z, Y()


        for sub in child_models:
            xm.blender.render.set_cycles(w=config.getint('DEFAULT', 'img_size'),
                                         h=config.getint('DEFAULT', 'img_size'))

            pitch, yaw, scale, hdr_name=split_model_name(sub)

            # Remove existing cameras and lights, if any
            for o in bpy.data.objects:
                o.select = o.type in ('LAMP', 'CAMERA')
            bpy.ops.object.delete()
            bpy.context.scene.update()

            for o in bpy.data.objects:
                if o.type == 'MESH':
                    o.select = True

            # Rotate Obj
            xm.blender.object.rotate_object(rotate_angle=math.pi / 180*pitch, rotate_axis=(True, False, False))
            xm.blender.object.rotate_object(rotate_angle=math.pi / 180*yaw, rotate_axis=(False, True, False))
            xm.blender.object.scale_object(scale=(scale,scale,scale),scale_axis=(True,True,True))

            # loading cam and light
            with open(os.path.join(config.get('DEFAULT', 'camera_path'), 'P01.json'), 'r') as h:
                cam = json.load(h)

            cam_obj = xm.blender.camera.add_camera(
                xyz=cam['position'], rot_vec_rad=cam['rotation'],
                name=cam['name'], f=cam['focal_length'],
                sensor_width=cam['sensor_width'], sensor_height=cam['sensor_height'],
                clip_start=cam['clip_start'], clip_end=cam['clip_end'])

            xm.blender.light.add_light_env(env=os.path.join(hdr_root_path,hdr_name+'.hdr'))

            xm.blender.render.easyset(n_samples=config.getint('DEFAULT','samples'), color_mode='RGB')
            bpy.context.scene.use_nodes = True

            # Saving Render results
            target_path = os.path.join(config.get('DEFAULT', 'save_path'), model,sub)
            if not os.path.exists(target_path):
                os.makedirs(target_path)

            xm.blender.render.render_shading(target_path)

            # Reset Obj
            xm.blender.object.rotate_object(rotate_angle=-math.pi / 180 * yaw, rotate_axis=(False, True, False))
            xm.blender.object.rotate_object(rotate_angle=-math.pi / 180 * pitch,
                                            rotate_axis=(True, False, False))
            xm.blender.object.scale_object(scale=(1.0/scale, 1.0/scale, 1.0/scale), scale_axis=(True, True, True))

        for o in bpy.data.objects:
            if o.type == 'MESH':
                o.select = True
        bpy.ops.object.delete()
        bpy.context.scene.update()

    # xm.blender.scene.save_blend('./blender.blend')

if __name__ == '__main__':
    main()
