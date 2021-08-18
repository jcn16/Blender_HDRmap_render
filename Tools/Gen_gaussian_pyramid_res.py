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
        if hdr.endswith('.exr'):
            continue
        print(hdr)
        gaussian=cn.hdr.Pyramids.Pyramids(image_path=os.path.join(root,hdr),levels=8)
        g=gaussian.gaussian_pyramid()[-1]
        g=g.astype("float32")
        save_path=os.path.join(target,hdr)
        cn.io.save_files.save_hdr(path=save_path,files=g)


if __name__=='__main__':
    root='/media/jcn/新加卷/JCN/JCN_test_datset/HDR_Heaven/HDRI_8k'
    target='/media/jcn/新加卷/JCN/JCN_test_datset/HDR_Heaven/HDRI_8k_pyramids'
    all_hdrs=os.listdir(root)
    all_hdrs.sort()

    pyramids_hdrs=os.listdir(target)
    pyramids_hdrs.sort()

    res=list(set(all_hdrs)^set(pyramids_hdrs))

    all_hdrs=res

    threads = []
    num_threads = 4
    split = int(len(all_hdrs) / num_threads)

    for i in range(num_threads):
        if i == (num_threads - 1):
            hdr_subs = all_hdrs[i * split:len(all_hdrs)]
        else:
            hdr_subs = all_hdrs[i * split:(i + 1) * split]

        t = threading.Thread(target=ComputePyramids, args=(hdr_subs,))
        threads.append(t)

    for t in threads:
        t.setDaemon(True)
        t.start()

    for t in threads:
        t.join()

