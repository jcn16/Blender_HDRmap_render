import cv2
import numpy as np

shadow='/media/jcn/新加卷/JCN/JCN_test_datset/RayTracing/Val/126111539896325-h/0_-32_0.8_9C4A9426-f14f216510/render.png'
unshadow='/media/jcn/新加卷/JCN/JCN_test_datset/RayTracing/Val/126111539896325-h/0_-32_0.8_9C4A9426-f14f216510/unshadow.png'

shadow=cv2.imread(shadow)
unshadow=cv2.imread(unshadow)

print(shadow.min(),shadow.max())
print(unshadow.min(),unshadow.max())

res=np.asarray(shadow)-np.asarray(unshadow)
print(res.min(),res.max())

cv2.imshow('iamge',res)
cv2.waitKey(0)