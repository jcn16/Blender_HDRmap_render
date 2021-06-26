import os
import shutil
from tqdm import tqdm

root='/media/jcn/新加卷/JCN/JCN_test_datset/train_semantic'
target='/media/jcn/新加卷/JCN/JCN_test_datset/Train_512'

child_dirs=os.listdir(root)
child_dirs.sort()
pbar=tqdm(total=len(child_dirs))

for model in child_dirs:
    pbar.update(1)
    sub_dirs=os.listdir(os.path.join(root,model))
    sub_dirs.sort()
    for dir in sub_dirs:
        src=os.path.join(root,model,dir,'semantic_mask.png')
        dst=os.path.join(target,model,dir,'semantic_mask.png')
        shutil.copyfile(src,dst)