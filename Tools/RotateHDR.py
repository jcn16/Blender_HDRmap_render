import chaonanlib as cn
from glob import glob
from tqdm import tqdm
import imageio


if __name__ == '__main__':

  # open source image
  root_path = "/media/jcn/新加卷/JCN/JCN_test_datset/HDR_Heaven/HDRI_8k/paul_lobe_haus_8k_36.hdr"

  src_image = cn.io.read_files.read_hdr(root_path)
  h, w, c = src_image.shape

  equirectRot1 = cn.hdr.EquirectRotate.EquirectRotate(h, w, (-36, 0, 0))
  rotated_image = equirectRot1.rotate(src_image)
  dst_path = "/media/jcn/新加卷/JCN/JCN_test_datset/HDR_Heaven/HDRI_8k/paul_lobe_haus_8k.hdr"
  cn.io.save_files.save_hdr(path=dst_path,files=rotated_image)



