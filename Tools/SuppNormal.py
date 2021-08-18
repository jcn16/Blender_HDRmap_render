import os,sys
import json
import shutil
from tqdm import tqdm

root='/media/jcn/新加卷/JCN/JCN_test_datset/RayTracing/Train_HDR_512'
target='/media/jcn/新加卷/JCN/JCN_test_datset/RayTracing/supp'

with open('./normal_supp.json','r') as f:
    normals=json.load(f)

pbar=tqdm(total=len(normals))

for normal in normals:
    pbar.update(1)
    model=normal.split('+')[0]
    dir=normal.split('+')[1]
    normal_path=os.path.join(root,model,dir,'normal.png')
    dst=os.path.join(target,model,dir)
    if not os.path.exists(dst):
        os.makedirs(dst)
    shutil.copyfile(normal_path,os.path.join(dst,'normal.png'))
