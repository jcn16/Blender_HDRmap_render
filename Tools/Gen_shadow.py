import cv2
import os
import numpy as np

root='/media/jcn/新加卷/JCN/JCN_test_datset/RayTracing/Train_HDR_512/137611541778263-h/0_16_1.1_kloppenheim_04_8k_36'
shadow=cv2.imread(os.path.join(root,'render.png'))
shadow=shadow/255.0
unshadow=cv2.imread(os.path.join(root,'unshadow.png'))
unshadow=unshadow/255.0

res=shadow/unshadow
res=np.asarray(np.clip(res*255,0,255),dtype=np.uint8)
res=cv2.medianBlur(res,5)
res=cv2.dilate(res,kernel=3,iterations=1)
res=cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)

cv2.imshow('res',res)
cv2.waitKey(0)