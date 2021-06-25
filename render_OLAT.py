import sys
import json
import os
from configparser import ConfigParser

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
    if not os.path.exists(config.get('DEFAULT','save_path')):
        os.makedirs(config.get('DEFAULT','save_path'))

    lights=os.listdir(config.get('DEFAULT','light_path'))
    lights.sort()

    # loading obj
    bpy.ops.import_scene.obj(filepath=config.get('DEFAULT', 'obj_path'),
                             axis_forward='-Z', axis_up='Y', filter_glob="*.obj;*.mtl")  # -Z, Y()

    for light_name in lights:
        # model path
        xm.blender.render.set_cycles(w=config.getint('DEFAULT','img_size'),h=config.getint('DEFAULT','img_size'))
        # Remove existing cameras and lights, if any
        for o in bpy.data.objects:
            o.select = o.type in ('LAMP', 'CAMERA')
        # for obj in bpy.context.scene.objects:
        #     obj.select=True
        bpy.ops.object.delete()
        '''
        for obj in bpy.context.scene.objects:
            print(obj.name)
            if obj.name in ['Lamp', 'Camera', 'light']:
                obj.select = True
            else:
                obj.select = False
        bpy.ops.object.delete()
        '''
        bpy.context.scene.update()

        for o in bpy.data.objects:
            if o.type=='MESH':
                o.select=True

        # loading cam and light
        with open(os.path.join(config.get('DEFAULT','camera_path'),'C14.json'), 'r') as h:
            cam = json.load(h)
        with open(os.path.join(config.get('DEFAULT','light_path'), light_name), 'r') as h:
            light = json.load(h)

        cam_obj = xm.blender.camera.add_camera(
            xyz=cam['position'], rot_vec_rad=cam['rotation'],
            name=cam['name'], f=cam['focal_length'],
            sensor_width=cam['sensor_width'], sensor_height=cam['sensor_height'],
            clip_start=cam['clip_start'], clip_end=cam['clip_end'])
        xm.blender.light.add_light_point(
            xyz=light['position'], name=light['name'], size=light['size'])
        # xm.blender.light.add_light_env(env='./9C4A0003-e05009bcad_tone.hdr')

        xm.blender.render.easyset(n_samples=64, color_mode='RGB')

        bpy.context.scene.use_nodes = True

        # rgb_camspc_f = os.path.join(config.get('DEFAULT','save_path'),light_name.split('.')[0]+'.png')
        # xm.blender.render.render(rgb_camspc_f)
        # normal_f = os.path.join('./normal')
        # xm.blender.render.render_normal(normal_f)
        alpha_f = os.path.join('./alpha.png')
        xm.blender.render.render_alpha(alpha_f,samples=64)
        # depth_f=os.path.join('./depth')
        # xm.blender.render.render_depth(depth_f)
        # light_f = os.path.join('./light')
        # xm.blender.render.render_lighting_passes(light_f)
        # AO_f = os.path.join('./AO.png')
        # xm.blender.render.render_ambient(AO_f)
        # albedo_f = os.path.join('./albedo.png')
        # xm.blender.render.render_albedo(albedo_f)

    # xm.blender.scene.save_blend('./blender.blend')


if __name__ == '__main__':
    main()
