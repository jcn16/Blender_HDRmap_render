from configparser import ConfigParser
import imageio
import OpenEXR
import Imath
import numpy

def read_ini(path):
    """
    read .ini config
    """
    config = ConfigParser()
    with open(path, 'r') as h:
        config.read_file(h)
    return config

def read_hdr(path):
    assert path.endswith('.hdr'), "Please input .hdr files"
    image=imageio.imread(path,format='HDR-FI')
    return image

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
    rgb = [numpy.fromstring(File.channel(c, PixType), dtype=numpy.float32) for c in 'RGB']
    r = numpy.reshape(rgb[0], (Size[1], Size[0]))
    g = numpy.reshape(rgb[1], (Size[1], Size[0]))
    b = numpy.reshape(rgb[2], (Size[1], Size[0]))
    hdr = numpy.zeros((Size[1], Size[0], 3), dtype=numpy.float32)
    hdr[:, :, 0] = r
    hdr[:, :, 1] = g
    hdr[:, :, 2] = b
    return hdr