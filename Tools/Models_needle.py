import os,sys
import shutil
from tqdm import tqdm

root='/mnt/nas/TwinDom/TwinDom_PerspectRandom_Noisy'
target='/home/jcn/图片/Twindom_images'

child_dirs=os.listdir(root)
child_dirs.sort()
pbar=tqdm(total=len(child_dirs))

for dir in child_dirs:
    pbar.update(1)
    src=os.path.join(root,dir,'color_view_0.jpg')
    dst=os.path.join(target,dir+'.jpg')
    shutil.copyfile(src,dst)