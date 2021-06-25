import chaonanlib as cn
from glob import glob
from tqdm import tqdm
import imageio


if __name__ == '__main__':

  # open source image
  root_path = "/media/jcn/新加卷/JCN/JCN_test_datset/HDR_Heaven/outdoor_HDRI"
  hdr_maps=glob(root_path+'/*.hdr')
  hdr_maps.sort()
  pbar=tqdm(total=len(hdr_maps))

  for hdr in hdr_maps:
    pbar.update(1)
    try:
        src_image=cn.io.read_files.read_hdr(hdr)
    except:
        print(hdr)
        continue
    h, w, c = src_image.shape

    # rotate source image
    for i in range(9):

      equirectRot1 = cn.hdr.EquirectRotate.EquirectRotate(h, w, ((i+1)*36, 0, 0))
      rotated_image = equirectRot1.rotate(src_image)
      dst_path = hdr.split('.')[0]+f'_{(i+1)*36}.hdr'
      cn.io.save_files.save_hdr(path=dst_path,files=rotated_image)



