import os,sys
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
import chaonanlib as cn
from tqdm import tqdm
from glob import glob
import threading
import imageio

def ComputeTone(hdrs):
    pbar=tqdm(total=len(hdrs))
    for hdr in hdrs:
        pbar.update(1)
        hdr_maps=cn.io.read_files.read_hdr(hdr)
        tone=cn.io.exr2hdr.TonemapHDR()
        hdr_maps_tone=tone(hdr_maps,clip=False)
        save_path=os.path.join(target,hdr.split('/')[-1])
        cn.io.save_files.save_hdr(path=save_path,files=hdr_maps_tone)

if __name__=='__main__':
    root='/media/jcn/新加卷/JCN/JCN_test_datset/IndoorHDRDataset_hdr'
    target='/media/jcn/新加卷/JCN/JCN_test_datset/IndoorHDRDataset_hdr_tone'
    all_hdrs=glob(root+'/*.hdr')
    all_hdrs.sort()

    threads=[]
    num_threads=5
    split=int(len(all_hdrs)/num_threads)

    for i in range(num_threads):
        if i==(num_threads-1):
            hdr_subs=all_hdrs[i*split:len(all_hdrs)]
        else:
            hdr_subs=all_hdrs[i*split:(i+1)*split]

        t=threading.Thread(target=ComputeTone,args=(hdr_subs,))
        threads.append(t)

    for t in threads:
        t.setDaemon(True)
        t.start()

    for t in threads:
        t.join()
