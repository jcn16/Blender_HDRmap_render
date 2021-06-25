import imageio
import numpy as np
import cv2
import chaonanlib as cn

exr2hdr=cn.io.exr2hdr.exr2hdr(input_path='../HDRmaps/9C4A0003-e05009bcad.exr', out_path='../HDRmaps/9C4A0003-e05009bcad_tone.hdr', use_tonemap=True)
exr2hdr.forward()


# print(img_1.shape)
# print(img_1.min(),img_1.max())
# image=np.asarray(np.clip(img_1[:,:,0:1]*255,0,255),dtype=np.uint8)
# cv2.imshow('image',image)
# cv2.waitKey(0)


