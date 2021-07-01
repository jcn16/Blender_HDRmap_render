import cv2
import numpy as np

image_1=cv2.imread('/media/jcn/新加卷/JCN/JCN_test_datset/Train_HDR_512/141311549049327-h/0_0_0.8_rural_winter_roadside_8k_72.png')
image_2=cv2.imread('/media/jcn/新加卷/JCN/JCN_test_datset/Train_HDR_512/141311549049327-h/0_0_0.8_storeroom_8k_252.png')

res=image_1/image_2

res=np.asarray(np.clip(res*255,0,255),dtype=np.uint8)
cv2.imshow('image',res)
cv2.waitKey(0)