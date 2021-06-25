import json
import os
import random

root='/media/jcn/新加卷/JCN/CLOTHES/Blender_rendering/metas/Oppo/models/train.json'
target='/media/jcn/新加卷/JCN/CLOTHES/Blender_rendering/metas/Oppo/models'
with open(root,'r') as f:
    models=json.load(f)

random.shuffle(models)

split_num=20
patches=int(len(models)/split_num)

for i in range(20):
    sub_models=models[i*patches:(i+1)*patches]
    dumps = json.dumps(sub_models, ensure_ascii=False, indent=4)

    cam_name = f'train_{i}.json'
    with open(os.path.join(target, cam_name), 'w') as f:
        f.write(dumps)