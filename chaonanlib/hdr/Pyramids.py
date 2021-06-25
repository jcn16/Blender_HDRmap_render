import matplotlib.pyplot as plt
import numpy as np
import imageio

from scipy.signal import convolve2d

class Pyramids:
    """
    @ image_path: endwith .hdr, .png , etc
    @ levels: pyramid levels
    @ gaussian_pyramid:a list of numpy arrays
    """
    def __init__(self,image_path,levels=4):
        self.kernel = self.smooth_gaussian_kernel(0.4)
        self.levels = levels
        if image_path.endswith('.hdr'):
            self.image=imageio.imread(image_path,format='HDR-FI')
        else:
            self.image=self.convert_image_to_floats(plt.imread(image_path))
    # Useful tools
    def convolve(self,image, kernel):
        """
        A fonction to perform a 2D convolution operation over an image using a chosen kernel.

        :param image: The grayscale image we want to use of dimension (N,M)
        :param kernel: The convolution kernel of dimention (k,k)
        :return: The convolved image of dimension (N,M)
        """
        im_out = convolve2d(image, kernel, mode='same', boundary='symm')
        return im_out

    def downsample(self,image, kernel):
        """
        A function to downsample an image.

        :param image: The grayscale image we want to use of dimension (N,M)
        :param kernel: The Gaussian blurring kernel of dimention (k,k)
        :return: The downsampled image of dimension (N/factor,M/factor)
        """
        blur_image = self.convolve(image, kernel)
        img_downsampled = blur_image[::2, ::2]
        return img_downsampled

    def upsample(self,image):
        """

        :param image: The grayscale image we want to use of dimension (N,M)
        :param factor: The upsampling factor, an integer
        :return: The upsampled image of dimension (N*factor,M*factor)
        """

        #kernel = np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]])/12
        kernel = self.smooth_gaussian_kernel(0.4)

        img_upsampled = np.zeros((image.shape[0]*2, image.shape[1]*2), dtype=np.float64)
        img_upsampled[::2, ::2] = image[:, :]
        img_upsampled = 4 * self.convolve(img_upsampled, kernel)
        return img_upsampled

    def classical_gaussian_kernel(self,k, sigma):
        """
        A function to generate a classical Gaussian kernel

        :param k: The size of the kernel, an integer
        :param sigma: variance of the gaussian distribution
        :return: A Gaussian kernel, a numpy array of shape (k,k)
        """
        w = np.linspace(-(k - 1) / 2, (k - 1) / 2, k)
        x, y = np.meshgrid(w, w)
        kernel = 0.5*np.exp(-0.5*(x**2 + y**2)/(sigma**2))/(np.pi*sigma**2)
        return kernel

    def smooth_gaussian_kernel(self,a):
        """
         A 5*5 gaussian kernel to perform smooth filtering.

        :param a: the coefficient of the smooth filter. A float usually within [0.3, 0.6]
        :return: A smoothing Gaussian kernel, a numpy array of shape (5,5)
        """
        w = np.array([0.25 - a/2.0, 0.25, a, 0.25, 0.25 - a/2.0])
        kernel = np.outer(w, w)
        return kernel

    def convert_image_to_floats(self,image):
        """
        A function to convert an image to a numpy array of floats within [0, 1]

        :param image: The image to be converted
        :return: The converted image
        """

        if np.max(image) <= 1.0:
            return image
        else:
            return image / 255.0

    # Build Pyramids
    def gaussian_pyramid(self):
        """
        A function to create a Gaussian pyramid of a defined number of levels and from a chosen kernel.

        :param image: The image we want to use of dimension (N,M,3) or (M,N)
        :param kernel: The Gaussian kernel of dimention (k,k)
        :param levels: The desired number of levels in the Gaussian pyramid, an integer
        :return: The Gaussian pyramid, a list of numpy arrays
        """

        if len(np.shape(self.image)) == 3:
            gauss_l_r = self.image[:, :, 0]
            gauss_l_g = self.image[:, :, 1]
            gauss_l_b = self.image[:, :, 2]
        gauss_l = self.image
        pyramid = [gauss_l]
        for l in range(self.levels):
            if len(np.shape(self.image)) == 3:
                # channels last format
                gauss_l_r = self.downsample(gauss_l_r, self.kernel)
                gauss_l_g = self.downsample(gauss_l_g, self.kernel)
                gauss_l_b = self.downsample(gauss_l_b, self.kernel)
                gauss_l = np.zeros((gauss_l_b.shape[0], gauss_l_b.shape[1], 3))
                gauss_l[:, :, 0] = gauss_l_r
                gauss_l[:, :, 1] = gauss_l_g
                gauss_l[:, :, 2] = gauss_l_b
            else:
                gauss_l = self.downsample(gauss_l, self.kernel)
            pyramid.append(gauss_l)
        return pyramid

    def laplacian_pyramid(self):
        """
        A function to create a Laplacian pyramid of a defined number of levels and from a chosen kernel.

        :param image: The image we want to use of dimension (N,M,3) or (M,N)
        :param kernel: The Gaussian kernel of dimention (k,k)
        :param levels: The desired number of levels in the Laplacian pyramid, an integer
        :return: The Laplacian pyramid, a list of numpy arrays
        """

        gauss = self.gaussian_pyramid()
        pyramid = []
        for l in range(len(gauss) - 2, -1, -1):
            if len(np.shape(self.image)) == 3:
                # channels last format
                gauss_l1r = self.upsample(gauss[l+1][:, :, 0])
                gauss_l1g = self.upsample(gauss[l+1][:, :, 1])
                gauss_l1b = self.upsample(gauss[l+1][:, :, 2])
                if gauss_l1r.shape[0] > gauss[l][:, :, 0].shape[0]:
                    gauss_l1r = np.delete(gauss_l1r, -1, axis=0)
                    gauss_l1g = np.delete(gauss_l1g, -1, axis=0)
                    gauss_l1b = np.delete(gauss_l1b, -1, axis=0)
                if gauss_l1r.shape[1] > gauss[l][:, :, 0].shape[1]:
                    gauss_l1r = np.delete(gauss_l1r, -1, axis=1)
                    gauss_l1g = np.delete(gauss_l1g, -1, axis=1)
                    gauss_l1b = np.delete(gauss_l1b, -1, axis=1)
                lap_l_r = gauss[l][:, :, 0] - gauss_l1r
                lap_l_g = gauss[l][:, :, 1] - gauss_l1g
                lap_l_b = gauss[l][:, :, 2] - gauss_l1b
                lap_l = np.zeros((lap_l_r.shape[0], lap_l_r.shape[1], 3))
                lap_l[:, :, 0] = lap_l_r
                lap_l[:, :, 1] = lap_l_g
                lap_l[:, :, 2] = lap_l_b
            else:
                gauss_l1 = self.upsample(gauss[l+1])
                if gauss_l1.shape[0] > gauss[l].shape[0]:
                    gauss_l1 = np.delete(gauss_l1, -1, axis=0)
                if gauss_l1.shape[1] > gauss[l].shape[1]:
                    gauss_l1 = np.delete(gauss_l1, -1, axis=1)
                lap_l = gauss[l] - gauss_l1
            pyramid.append(lap_l)
        return pyramid

