import cv2
import numpy as np


def tianchong(img):
    m = img.shape[0]
    n = img.shape[1]
    append = int(np.ceil(abs(m - n) / 2))
    if m > n:
        constant = cv2.copyMakeBorder(img, 0, 0, append, append, cv2.BORDER_CONSTANT, value=(0, 0, 0))
    else:
        constant = cv2.copyMakeBorder(img, append, append, 0, 0, cv2.BORDER_CONSTANT, value=(0, 0, 0))
    constant = cv2.resize(constant, (512, 512))
    return constant

def compare():
    image_1=cv2.imread('/media/jcn/新加卷/JCN/JCN_test_datset/RayTracing/Train_HDR_512/126111539900259-h/0_-32_1_dikhololo_sunset_8k_324/raytracing.png')
    mask_1=cv2.imread('/media/jcn/新加卷/JCN/JCN_test_datset/RayTracing/Train_HDR_512/126111539900259-h/0_-32_1_dikhololo_sunset_8k_324/alpha.png')
    image_1=tianchong(image_1)
    mask_1=tianchong(mask_1)

    image_2=cv2.imread('/media/jcn/新加卷/JCN/JCN_test_datset/RayTracing/Train_HDR_512/126111539900259-h/0_-32_1_dikhololo_sunset_8k_324/shading.png')

    image_1=image_1/255.0*mask_1/255.0
    image_2=image_2/255.0*mask_1/255.0
    cv2.imshow('image_1',np.asarray(image_1*255,dtype=np.uint8))
    cv2.imshow('image_2',np.asarray(image_2*255,dtype=np.uint8))


    res=np.asarray(np.clip((image_1-image_2)*255,0,255),dtype=np.uint8)
    cv2.imshow('res',res)
    cv2.waitKey(0)

def composite():
    shading=cv2.imread('/media/jcn/新加卷/JCN/RelightHDR/TEST/images_high_res/10/raytracing.png')
    albedo=cv2.imread('/home/jcn/桌面/Oppo/Results_albedo/10/p_albedo.png')
    mask=cv2.imread('/home/jcn/桌面/Oppo/Results_albedo/10/gt_mask.png')

    relight=albedo/255.0*shading/255.0*mask/255.0
    relight=np.asarray(relight*255,dtype=np.uint8)

    cv2.imshow('relight',relight)
    cv2.waitKey(0)

if __name__=='__main__':
    compare()


