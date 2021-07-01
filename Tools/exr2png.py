import chaonanlib as cn
import os,sys
import numpy as np
import cv2
from tqdm import tqdm

def TransNormal(dir_path):
    normal=cn.io.read_files.read_exr(os.path.join(dir_path,'normal.exr'))
    R=normal[:,:,1:2]
    G=normal[:,:,0:1]
    B=-normal[:,:,2:3]
    new_normal=np.concatenate([R,G,B],axis=2)
    new_normal=np.asarray(np.clip((0.5*new_normal+0.5)*255,0,255),dtype=np.uint8)
    cv2.imwrite(os.path.join(dir_path,'normal.png'),new_normal[:,:,::-1])

root='/media/jcn/新加卷/JCN/JCN_test_datset/Train_HDR_512'
model_dirs=os.listdir(root)
model_dirs.sort()
pbar=tqdm(total=len(model_dirs))

for model in model_dirs:
    pbar.update(1)
    child_dirs=os.listdir(os.path.join(root,model))
    child_dirs.sort()
    for dir in child_dirs:
        dir_path=os.path.join(root,model,dir)
        TransNormal(dir_path)
