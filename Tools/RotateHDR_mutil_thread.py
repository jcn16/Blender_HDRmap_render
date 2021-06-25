import chaonanlib as cn
from glob import glob
import threading
from tqdm import tqdm
import imageio


if __name__ == '__main__':

    def ComputeHDR(hdr_maps):
        pbar=tqdm(total=len(hdr_maps))
        for hdr in hdr_maps:
            pbar.update(1)
            try:
                src_image = cn.io.read_files.read_hdr(hdr)
            except:
                print(hdr)
                continue
            h, w, c = src_image.shape

            # rotate source image
            for i in range(9):
              equirectRot1 = cn.hdr.EquirectRotate.EquirectRotate(h, w, ((i + 1) * 36, 0, 0))
              rotated_image = equirectRot1.rotate(src_image)
              dst_path = hdr.split('.')[0] + f'_{(i + 1) * 36}.hdr'
              cn.io.save_files.save_hdr(path=dst_path, files=rotated_image)

    # open source image
    root_path = "/media/jcn/新加卷/JCN/JCN_test_datset/HDR_Heaven/indoor_HDRI"
    hdr_maps=glob(root_path+'/*.hdr')
    hdr_maps.sort()

    threads=[]

    num_threads=5
    split=int(len(hdr_maps)/num_threads)

    for i in range(num_threads):
        if i==(num_threads-1):
            hdr_subs=hdr_maps[i*split:len(hdr_maps)]
        else:
            hdr_subs=hdr_maps[i*split:(i+1)*split]

        t=threading.Thread(target=ComputeHDR,args=(hdr_subs,))
        threads.append(t)

    for t in threads:
      t.setDaemon(True)
      t.start()

    for t in threads:
      t.join()





