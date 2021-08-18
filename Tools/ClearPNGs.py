import os
import glob
from tqdm import tqdm

def clearPNGs():
    root='/media/jcn/新加卷/JCN/JCN_test_datset/RayTracing/Val'
    child_models=os.listdir(root)
    child_models.sort()
    pbar=tqdm(total=len(child_models))

    for model in child_models:
        pbar.update(1)
        pngs=glob.glob(os.path.join(root,model)+'/*.png')
        for png in pngs:
            os.remove(os.path.join(root,model,png))


def clearPifuObjs():
    root = '/media/jcn/新加卷/JCN/JCN_test_datset/RayTracing/Val'
    child_models = os.listdir(root)
    child_models.sort()
    pbar = tqdm(total=len(child_models))

    for model in child_models:
        pbar.update(1)
        present_dir=os.path.join(root,model)
        sub_dirs=os.listdir(present_dir)
        sub_dirs.sort()

        for dir in sub_dirs:
            raytracing=os.path.join(root,model,dir,'raytracing.png')
            pifu_obj=os.path.join(root,model,dir,'pifu.obj')
            if os.path.exists(raytracing):
                os.remove(pifu_obj)

clearPNGs()
