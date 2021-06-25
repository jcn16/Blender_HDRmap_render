from configparser import ConfigParser
import imageio

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