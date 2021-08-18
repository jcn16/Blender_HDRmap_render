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

def main():
    # Open scene
    xm.blender.scene.open_blend('./test.blend')
    config=read_ini('./config.ini')
    if not os.path.exists(config.get('DEFAULT', 'save_path')):
        os.makedirs(config.get('DEFAULT', 'save_path'))

    # model path
    with open(os.path.join(config.get('DEFAULT', 'model_json_path'),'val.json'),'r') as f:
        child_models=json.load(f)
        child_models.sort()

    # rendered model
    rendered_models=os.listdir(config.get('DEFAULT', 'save_path'))

    # HDR map path
    child_maps=glob(config.get('DEFAULT', 'light_path')+'/*.hdr')
    child_maps.sort()

    # Loading models
    for model in child_models:
        if model in rendered_models:
            continue
        xm.blender.render.set_cycles(w=config.getint('DEFAULT','img_size'),h=config.getint('DEFAULT','img_size'))

        # loading obj
        obj_path = os.path.join(config.get('DEFAULT', 'root_path'), model, model.split('-')[0] + '_scaled.obj')
        bpy.ops.import_scene.obj(filepath=obj_path,
                                 axis_forward='-Z', axis_up='Y', filter_glob="*.obj;*.mtl")  # -Z, Y()

        for pitch in range(0,31,10):
            for yaw in range(-32,33,8):
                for scale in [0.8,1,1.1]:
                    for i in range(config.getint('DEFAULT','light_num')):
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

                        light_idx=random.randint(0,len(child_maps)-1)
                        xm.blender.light.add_light_env(env=child_maps[light_idx])

                        xm.blender.render.easyset(n_samples=config.getint('DEFAULT','samples'), color_mode='RGB')
                        bpy.context.scene.use_nodes = True

                        # Saving Render results
                        target_path = os.path.join(config.get('DEFAULT', 'save_path'), model,f'{pitch}_{yaw}_{scale}_{child_maps[light_idx].split("/")[-1].split(".")[0]}')
                        if not os.path.exists(target_path):
                            os.makedirs(target_path)

                        # print(target_path)

                        xm.blender.render.render_all_color(target_path)
                        normal_f = os.path.join(target_path, 'normal')
                        xm.blender.render.render_normal(normal_f)
                        alpha_f = os.path.join(target_path, 'alpha.png')
                        xm.blender.render.render_alpha(alpha_f, samples=config.getint('DEFAULT','samples'))
                        depth_f = os.path.join(target_path, 'depth')
                        xm.blender.render.render_depth(depth_f)


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
