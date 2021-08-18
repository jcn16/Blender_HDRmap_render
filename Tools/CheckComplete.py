import os
import json
import tqdm

def check_hdr():
    def split_model_name(name):
        pitch=int(name.split('_')[0])
        yaw=int(name.split('_')[1])
        scale=float(name.split('_')[2])

        camera_length=len(name.split('_')[0]+'_'+name.split('_')[1]+'_'+name.split('_')[2]+'_')
        hdr=name[camera_length:len(name)]

        return pitch,yaw,scale,hdr

    light='/media/jcn/新加卷/JCN/JCN_test_datset/RayTracing/HDRI_8k_pyramids'
    renders='/media/jcn/新加卷/JCN/JCN_test_datset/RayTracing/Train_HDR_512'

    lights=os.listdir(light)

    all=set()

    child_models=os.listdir(renders)
    child_models.sort()
    pbar=tqdm.tqdm(total=len(child_models))


    for model in child_models:
        pbar.update(1)
        sub_dirs=os.listdir(os.path.join(renders,model))
        count=0
        for dir in sub_dirs:
            try:
                _,_,_,dir_name=split_model_name(dir)
                dir_name = dir_name + '.hdr'
                if dir_name in lights:
                    continue
                else:
                    print(dir_name)
                    count += 1
                    all.add(dir_name)
            except:
                print(dir)

        print(count)

    print(all)
    print(len(all))

def check_normal():
    root='/media/jcn/新加卷/JCN/JCN_test_datset/RayTracing/Train_HDR_512'
    child_models=os.listdir(root)
    child_models.sort()
    pbar=tqdm.tqdm(total=len(child_models))
    for model in child_models:
        pbar.update(1)
        child_dirs=os.listdir(os.path.join(root,model))
        child_dirs.sort()
        for dir in child_dirs:
            normal_path=os.path.join(root,model,dir,'normal.png')
            if os.path.exists(normal_path):
                pass
            else:
                print(model+'+'+dir)

check_normal()