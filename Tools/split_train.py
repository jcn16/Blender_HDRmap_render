import json
import os
import random

def split_train():
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

def gen_res():
    """
    supply all models, num=1779-814
    """
    root = '/mnt/nas/TwinDom/TwinDom_PerspectRandom_Noisy'
    child_dirs = os.listdir(root)
    child_dirs.sort()

    with open('/media/jcn/新加卷/JCN/CLOTHES/Blender_rendering/metas/Oppo/models/train.json','r') as f:
        train=json.load(f)
    with open('/media/jcn/新加卷/JCN/CLOTHES/Blender_rendering/metas/Oppo/models/val.json','r') as f:
        val=json.load(f)

    print(len(train))
    print(len(val))
    exist=train+val
    res=list(set(exist)^set(child_dirs))
    print(len(res))

    dict=json.dumps(res,ensure_ascii = False, indent = 4)
    with open('/media/jcn/新加卷/JCN/CLOTHES/Blender_rendering/metas/Oppo/models/res.json', 'w') as f:
        f.write(dict)

def gen_json(path,save_path):
    child_dirs=os.listdir(path)
    all=[]
    for dir in child_dirs:
        all.append(dir.split('.')[0])
    all.sort()

    dict = json.dumps(all, ensure_ascii=False, indent=4)
    with open(save_path, 'w') as f:
        f.write(dict)

def gen_json_easy_res():
    with open('/media/jcn/新加卷/JCN/CLOTHES/Blender_rendering/metas/Oppo/models/res.json', 'r') as f:
        res = json.load(f)
    with open('/media/jcn/新加卷/JCN/CLOTHES/Blender_rendering/metas/Oppo/models/classify/easy.json', 'r') as f:
        easy = json.load(f)
    choosed = list(set(res).intersection(set(easy)))
    dict = json.dumps(choosed, ensure_ascii=False, indent=4)
    with open('/metas/Oppo/models/classify/easy_res.json', 'w') as f:
        f.write(dict)


gen_json_easy_res()