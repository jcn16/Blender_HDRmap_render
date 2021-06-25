import os,sys
import cv2
import numpy as np
from tqdm import tqdm

parse_dicts={
    # RGB value
    'hair':(0,128,0),
    'shirt':(128,0,128),
    'pants':(192,0,0),
    'dress':(0,128,128),
    'skirt':(64,0,128),
    'coat':(128,128,128),
    'shoes_left':(128,192,0),
    'shoes_right':(0,192,0),
}

def get_parts_mask(parts,image_old):
    image = np.asarray(image_old, dtype=np.int)
    image = np.reshape(image, (-1, 3))
    image = image - parse_dicts[parts]
    image = np.reshape(image, (512, 512, 3))
    image = np.asarray(image, dtype=np.uint8)
    image=np.sum(image,axis=2,keepdims=True)
    image=np.asarray(image<0.5,dtype=np.float)
    return image

def human_parsing(image,mask=None):
    """
    @ image: cv2.imread image,type=uint8,channel=RGB
    @ mask: float
    """
    mask_dict={}
    for key in parse_dicts.keys():
        mask_dict[key]=get_parts_mask(key,image)

    skin_mask=mask
    for key in mask_dict.keys():
        skin_mask=(skin_mask-mask_dict[key])

    mask_dict['skin']=skin_mask
    # add all mask
    color_dict = {
        'shoes_left': (255,0,0),
        'shoes_right': (255,0,0),
        'hair': (0,255,0),
        'shirt':(0,0,255),
        'skirt':(128,0,0),
        'pants':(128,128,0),
        'dress':(0,128,128),
        'coat': (128, 0, 128),
        'skin': (128,128,128)
    }
    final_semantic = np.repeat(mask_dict['skin'], 3, 2) * color_dict['skin']
    for key in mask_dict.keys():
        if key=='skin':
            continue
        final_semantic+=np.repeat(mask_dict[key], 3, 2) * color_dict[key]

    final_semantic=np.asarray(final_semantic,dtype=np.uint8)
    return final_semantic


root='/media/jcn/新加卷/JCN/JCN_test_datset/Train_512_semantic'
root_mask='/media/jcn/新加卷/JCN/JCN_test_datset/Train_512'
target='/media/jcn/新加卷/JCN/JCN_test_datset/semantic'

child_dirs=os.listdir(root)
child_dirs.sort()
pbar=tqdm(total=len(child_dirs))

for model in child_dirs:
    pbar.update(1)
    sub_dirs=os.listdir(os.path.join(root,model))
    sub_dirs.sort()
    for dir in sub_dirs:
        image=cv2.imread(os.path.join(root,model,dir,'semantic.png'))
        mask=cv2.imread(os.path.join(root_mask,model,dir,'mask.png'),flags=2)
        mask=mask/255.0
        final = human_parsing(image[:, :, ::-1], mask[:, :, None])
        # save semantic
        target_path=os.path.join(target,model,dir)
        if not os.path.exists(target_path):
            os.makedirs(target_path)

        cv2.imwrite(os.path.join(target_path,'semantic_mask.png'),final[:,:,::-1])
