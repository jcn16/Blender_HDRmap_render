import os,sys
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
import xiuminglib as xm
import numpy as np
import cv2


exr=xm.io.exr.EXR(exr_path='/media/jcn/新加卷/JCN/CLOTHES/Blender_rendering/render_results/normal.exr')
exr.extract_rgb(outpath='/media/jcn/新加卷/JCN/CLOTHES/Blender_rendering/render_results/normal.npy')

normal=np.load('/media/jcn/新加卷/JCN/CLOTHES/Blender_rendering/render_results/normal.npy')
normal=np.clip((0.5*normal+0.5)*255,0,255)
normal=np.asarray(normal,dtype=np.uint8)
cv2.imshow('normal',normal)
cv2.waitKey(0)
