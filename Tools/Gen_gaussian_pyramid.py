import os,sys
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
import chaonanlib as cn
from tqdm import tqdm
from glob import glob
import threading

def ComputePyramids(hdrs):
    pbar=tqdm(total=len(hdrs))
    for hdr in hdrs:
        pbar.update(1)
        gaussian=cn.hdr.Pyramids.Pyramids(image_path=hdr,levels=8)
        g=gaussian.gaussian_pyramid()[-1]
        g=g.astype("float32")
        save_path=os.path.join(target,hdr.split('/')[-1])
        cn.io.save_files.save_hdr(path=save_path,files=g)

if __name__=='__main__':
    root='/media/jcn/新加卷/JCN/JCN_test_datset/HDR_Heaven/HDRI_8k'
    target='/media/jcn/新加卷/JCN/JCN_test_datset/HDR_Heaven/HDRI_8k_pyramids'
    all_hdrs=glob(root+'/*.hdr')
    all_hdrs.sort()

    threads=[]
    num_threads=8
    split=int(len(all_hdrs)/num_threads)

    for i in range(num_threads):
        if i==(num_threads-1):
            hdr_subs=all_hdrs[i*split:len(all_hdrs)]
        else:
            hdr_subs=all_hdrs[i*split:(i+1)*split]

        t=threading.Thread(target=ComputePyramids,args=(hdr_subs,))
        threads.append(t)

    for t in threads:
        t.setDaemon(True)
        t.start()

    for t in threads:
        t.join()
