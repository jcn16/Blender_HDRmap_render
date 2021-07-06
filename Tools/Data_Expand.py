import Augmentor
from PIL import Image
import numpy as np
import os

def load_images(path):
    '''

    Args:
        path: path to save muti-tasks images

    Returns:
        [[render,depth,mask,...],
         [render,depth,mask,...]]

    '''
    render=np.asarray(Image.open(os.path.join(path,'render.png')))
    mask=np.asarray(Image.open(os.path.join(path,'alpha.png')))
    ambient=np.asarray(Image.open(os.path.join(path,'ambient.png')))
    albedo=np.asarray(Image.open(os.path.join(path,'albedo.png')))
    normal=np.asarray(Image.open(os.path.join(path,'normal.png')))

    data=[[render,mask,normal,ambient,albedo]]
    return data

images=load_images('/home/jcn/图片/0_0_0.8_nagoya_wall_path_8k_216')
p = Augmentor.DataPipeline(images)
p.zoom_random(1, percentage_area=0.8)
p.resize(probability=1.0, width=512, height=512)

augmented_images= p.sample(10)

for i in range(10):
    render_0=Image.fromarray(augmented_images[i][0])
    mask_0=Image.fromarray(augmented_images[i][1])
    normal_0=Image.fromarray(augmented_images[i][2])
    ambient_0=Image.fromarray(augmented_images[i][3])
    albedo_0=Image.fromarray(augmented_images[i][4])
    render_0.save(f'/home/jcn/图片/0_0_0.8_nagoya_wall_path_8k_216/render_{i}.png')
    mask_0.save(f'/home/jcn/图片/0_0_0.8_nagoya_wall_path_8k_216/mask_{i}.png')
    normal_0.save(f'/home/jcn/图片/0_0_0.8_nagoya_wall_path_8k_216/normal_{i}.png')
    ambient_0.save(f'/home/jcn/图片/0_0_0.8_nagoya_wall_path_8k_216/ambient_{i}.png')
    albedo_0.save(f'/home/jcn/图片/0_0_0.8_nagoya_wall_path_8k_216/albedo_{i}.png')


