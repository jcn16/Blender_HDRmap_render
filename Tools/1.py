import os
import shutil

root='/home/jcn/图片/real_images'
child_images=os.listdir(os.path.join(root,'real'))
child_images.sort()

count=20
for image in child_images:
    src=os.path.join(root,'real',image)
    name=str(count)+'.'+image.split('.')[-1]
    dst=os.path.join(root,name)
    shutil.copyfile(src,dst)
    count+=1
