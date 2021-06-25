import xiuminglib as xm
import os
import cv2
import numpy as np

path='/media/jcn/新加卷/JCN/JCN_test_datset/IndoorHDRDataset_exr/9C4A3397-70d1e2f658.exr'
exr=xm.io.exr.EXR(exr_path=path)
data=exr.load()
print(data['B'].shape)
print(data['B'].min(),data['R'].max())

