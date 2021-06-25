import numpy
import OpenEXR
import Imath
import imageio
import glob
import os
import numpy as np

class exr2hdr:
    '''
    @input_path: endwith .exr
    @out_path: endwith .hdr
    '''
    def __init__(self,input_path,out_path,use_tonemap=False):
        self.input_path=input_path
        self.out_path=out_path
        self.use_tonemap=use_tonemap

    def gethdr(self):
        File = OpenEXR.InputFile(self.input_path)
        PixType = Imath.PixelType(Imath.PixelType.FLOAT)
        DW = File.header()['dataWindow']
        Size = (DW.max.x - DW.min.x + 1, DW.max.y - DW.min.y + 1)
        rgb = [numpy.fromstring(File.channel(c, PixType), dtype=numpy.float32) for c in 'RGB']
        r =numpy.reshape(rgb[0],(Size[1],Size[0]))
        g =numpy.reshape(rgb[1],(Size[1],Size[0]))
        b =numpy.reshape(rgb[2],(Size[1],Size[0]))
        self.hdr = numpy.zeros((Size[1],Size[0],3),dtype=numpy.float32)
        self.hdr[:,:,0] = r
        self.hdr[:,:,1] = g
        self.hdr[:,:,2] = b
        if self.use_tonemap:
            tone=TonemapHDR()
            self.hdr=tone(self.hdr,False)
        return self.hdr

    def writehdr(self):
        imageio.imwrite(self.out_path,self.hdr,format='hdr')

    def forward(self):
        hdr=self.gethdr()
        self.writehdr()

class TonemapHDR(object):
    """
        Tonemap HDR image globally. First, we find alpha that maps the (max(numpy_img) * percentile) to max_mapping.
        Then, we calculate I_out = alpha * I_in ^ (1/gamma)
        input : nd.array batch of images : [H, W, C]
        output : nd.array batch of images : [H, W, C]
    """

    def __init__(self, gamma=2.4, percentile=50, max_mapping=0.5):
        self.gamma = gamma
        self.percentile = percentile
        self.max_mapping = max_mapping  # the value to which alpha will map the (max(numpy_img) * percentile) to

    def __call__(self, numpy_img, clip=False, alpha=None, gamma=True):
        if gamma:
            power_numpy_img = np.power(numpy_img, 1 / self.gamma)
        else:
            power_numpy_img = numpy_img
        non_zero = power_numpy_img > 0
        if non_zero.any():
            r_percentile = np.percentile(power_numpy_img[non_zero], self.percentile)
        else:
            r_percentile = np.percentile(power_numpy_img, self.percentile)
        if alpha is None:
            alpha = self.max_mapping / (r_percentile + 1e-10)
        tonemapped_img = np.multiply(alpha, power_numpy_img)

        if clip:
            tonemapped_img = np.clip(tonemapped_img, 0, 1)

        return tonemapped_img.astype('float32')