import os,sys
import numpy as np
import cv2
import Imath
import OpenEXR
from tqdm import tqdm

def read_exr(path):
    """
    @ input: .exr path
    @ output: numpy [H,W,3]
    """
    assert path.endswith('.exr'), "Please input .exr files"
    File = OpenEXR.InputFile(path)
    PixType = Imath.PixelType(Imath.PixelType.FLOAT)
    DW = File.header()['dataWindow']
    Size = (DW.max.x - DW.min.x + 1, DW.max.y - DW.min.y + 1)
    rgb = [np.fromstring(File.channel(c, PixType), dtype=np.float32) for c in 'RGB']
    r = np.reshape(rgb[0], (Size[1], Size[0]))
    g = np.reshape(rgb[1], (Size[1], Size[0]))
    b = np.reshape(rgb[2], (Size[1], Size[0]))
    hdr = np.zeros((Size[1], Size[0], 3), dtype=np.float32)
    hdr[:, :, 0] = r
    hdr[:, :, 1] = g
    hdr[:, :, 2] = b
    return hdr

def TransNormal(dir_path):
    normal=read_exr(os.path.join(dir_path,'normal.exr'))
    R=-normal[:,:,0:1]
    G=-normal[:,:,1:2]
    B=-normal[:,:,2:3]
    new_normal=np.concatenate([R,G,B],axis=2)
    new_normal=np.asarray(np.clip((0.5*new_normal+0.5)*255,0,255),dtype=np.uint8)
    cv2.imshow('image',new_normal[:,:,::-1])
    cv2.waitKey(0)


dir_path='/media/jcn/新加卷/JCN/JCN_test_datset/RayTracing/Train_HDR_512/126111539901640-h/0_0_0.8_bell_park_dawn_8k_144'
TransNormal(dir_path)

