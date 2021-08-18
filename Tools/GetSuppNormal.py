import os,sys
import numpy as np
import json
from tqdm import tqdm

root='/media/jcn/新加卷/JCN/JCN_test_datset/RayTracing/Train_HDR_512'
model_dirs=os.listdir(root)
model_dirs.sort()
pbar=tqdm(total=len(model_dirs))

all=[]

for model in model_dirs:
    pbar.update(1)
    child_dirs=os.listdir(os.path.join(root,model))
    child_dirs.sort()
    for dir in child_dirs:
        if dir.endswith('.png'):
            continue
        normal_path=os.path.join(root,model,dir,'normal.png')
        if os.path.exists(normal_path):
            pass
        else:
            all.append(model+'+'+dir)

dumps=json.dumps(all,ensure_ascii=False, indent=4)
with open('./normal_supp.json','w') as f:
    f.write(dumps)
