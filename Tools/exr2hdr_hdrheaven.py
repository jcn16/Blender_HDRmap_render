import os
import chaonanlib as cn
import glob
import tqdm

root='/media/jcn/新加卷/JCN/JCN_test_datset/HDR_Heaven/outdoor_HDRI_4k'
target=root

exrs=glob.glob(root+'/*.exr')
exrs.sort()

pbar=tqdm.tqdm(total=len(exrs))

for exr in exrs:
    pbar.update(1)
    name=exr.split('/')[-1].split('.')[0]
    hdr=os.path.join(target,name+'.hdr')
    exr2hdr=cn.io.exr2hdr.exr2hdr(input_path=exr,out_path=hdr,use_tonemap=False)
    exr2hdr.forward()
