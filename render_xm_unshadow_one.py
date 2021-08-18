import sys
import json
import os
import math

# Blender
import bpy
sys.path.append(os.path.abspath((os.path.dirname(__file__))))

import xiuminglib as xm

def main():
    # Open scene
    xm.blender.scene.open_blend('./test.blend')

    # model path

    xm.blender.render.set_cycles(w=512,h=512)

    # Remove existing cameras and lights, if any
    for o in bpy.data.objects:
        o.select = o.type in ('LAMP', 'CAMERA')
    for obj in bpy.context.scene.objects:
        obj.select=True
    bpy.ops.object.delete()
    bpy.context.scene.update()

    # loading obj
    bpy.ops.import_scene.obj(filepath='./127711540134843-h/127711540134843_scaled.obj',
                             axis_forward='-Z', axis_up='Y', filter_glob="*.obj;*.mtl") #-Z, Y()

    # rotate obj
    # xm.blender.object.rotate_object(rotate_angle=math.pi/6,rotate_axis=(True,False,False))
    # xm.blender.object.rotate_object(rotate_angle=math.pi/2,rotate_axis=(False,True,False))
    # xm.blender.object.scale_object(scale=(1.1,1.1,1.1),scale_axis=(True,True,True))

    # loading cam and light
    with open('metas/Oppo/cams/P01.json', 'r') as h:
        cam = json.load(h)
    with open('metas/Olat/trainvali_lights/L001.json', 'r') as h:
        light = json.load(h)

    cam_obj = xm.blender.camera.add_camera(
        xyz=cam['position'], rot_vec_rad=cam['rotation'],
        name=cam['name'], f=cam['focal_length'],
        sensor_width=cam['sensor_width'], sensor_height=cam['sensor_height'],
        clip_start=cam['clip_start'], clip_end=cam['clip_end'])
    # xm.blender.light.add_light_env(env='/media/jcn/新加卷/JCN/CLOTHES/Blender_rendering/HDRmaps/round_platform_4k.hdr')
    xm.blender.light.add_light_point(
        xyz=light['position'], name=light['name'], size=light['size'])

    xm.blender.render.easyset(n_samples=64, color_mode='RGB')
    bpy.context.scene.use_nodes = True

    xm.blender.render.render_unshadow('/media/jcn/新加卷/JCN/CLOTHES/Blender_rendering/render_results')
    #
    # rgb_camspc_f = os.path.join('render_results/rgb.png')
    # xm.blender.render.render(rgb_camspc_f)
    # normal_f = os.path.join('render_results/normal')
    # xm.blender.render.render_normal(normal_f)
    #
    # alpha_f = os.path.join('render_results/alpha.png')
    # xm.blender.render.render_alpha(alpha_f,samples=64)
    # # depth_f=os.path.join('render_results/depth')
    # # xm.blender.render.render_depth(depth_f)
    # AO_f = os.path.join('render_results/AO.png')
    # xm.blender.render.render_ambient(AO_f)
    # albedo_f = os.path.join('render_results/albedo.png')
    # xm.blender.render.render_albedo(albedo_f)


    # xm.blender.object.rotate_object(rotate_angle=-math.pi / 2, rotate_axis=(False, True, False))
    # xm.blender.object.rotate_object(rotate_angle=-math.pi / 6, rotate_axis=(True, False, False))
    # xm.blender.object.scale_object(scale=(1.1, 1.1, 1.1), scale_axis=(True, True, True))

    # rgb_camspc_f = os.path.join('/media/jcn/新加卷/JCN/CLOTHES/Blender_rendering/render_results')
    # xm.blender.render.render(rgb_camspc_f)
    # normal_f = os.path.join('render_results/normal_1')
    # xm.blender.render.render_normal(normal_f)
    # alpha_f = os.path.join('render_results/alpha_1.png')
    # xm.blender.render.render_alpha(alpha_f, samples=64)
    # depth_f = os.path.join('render_results/depth_1')
    # xm.blender.render.render_depth(depth_f)
    # AO_f = os.path.join('render_results/AO_1.png')
    # xm.blender.render.render_ambient(AO_f)
    # albedo_f = os.path.join('render_results/albedo_1.png')
    # xm.blender.render.render_albedo(albedo_f)
    # xm.blender.scene.save_blend('./blend_1.blend')


if __name__ == '__main__':
    main()
