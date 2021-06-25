import os
import shutil

root='/media/jcn/新加卷/JCN/JCN_test_datset/Train_512_semantic'
target='/media/jcn/新加卷/JCN/JCN_test_datset/train_needle'

child_dirs=os.listdir(root)
for child in child_dirs:
    sub_dirs=os.listdir(os.path.join(root,child))
    sub_dirs.sort()

    src=os.path.join(root,child,sub_dirs[0],'semantic.png')
    dst=os.path.join(target,child+'.png')

    shutil.copyfile(src,dst)