import os,sys
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
import chaonanlib as cn
import cv2
import numpy as np

hdr=cn.io.read_files.read_hdr(path='/media/jcn/新加卷/JCN/JCN_test_datset/HDR_Heaven/HDRI_8k_pyramids/abandoned_hall_01_8k_72.hdr')
hdr=np.asarray(np.clip(hdr*255,0,255),dtype=np.uint8)

cv2.imshow('image',hdr[:,:,::-1])
cv2.waitKey(0)