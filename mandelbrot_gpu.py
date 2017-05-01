# 
# A CUDA version to calculate the Mandelbrot set
# Author: Hongting Chen
# Date: 04/30/2017
#
from numba import cuda
import numpy as np
from pylab import imshow, show

@cuda.jit(device=True)
def mandel(x, y, max_iters):
    '''
    Given the real and imaginary parts of a complex number,
    determine if it is a candidate for membership in the 
    Mandelbrot set given a fixed number of iterations.
    '''
    c = complex(x, y)
    z = 0.0j
    for i in range(max_iters):
        z = z*z + c
        if (z.real*z.real + z.imag*z.imag) >= 4:
            return i

    return max_iters

@cuda.jit
def compute_mandel(min_x, max_x, min_y, max_y, image, iters):
    '''
    Calculate the mandel value for each element in the 
    image array. The real and imag variables contain a 
    value for each element of the complex space defined 
    by the X and Y boundaries (min_x, max_x) and 
    (min_y, max_y).
    '''

    height = image.shape[0]
    width = image.shape[1]

    start_x, start_y = cuda.grid(2)

    # calculate the ending x and y coordinates 
    end_x = cuda.blockDim.x * cuda.gridDim.x
    end_y = cuda.blockDim.y * cuda.gridDim.y   

    pixel_size_x = (max_x - min_x) / width
    pixel_size_y = (max_y - min_y) / height

    #compute the mandel value for each element of the block
    for x in range(start_x, width, end_x):
        real = min_x + x * pixel_size_x
        for y in range(start_y, height, end_y):
            imag = min_y + y * pixel_size_y 
            image[y, x] = mandel(real, imag, iters)


if __name__ == '__main__':
    image = np.zeros((1024, 1536), dtype = np.uint8)
    blockdim = (32, 8)
    griddim = (32, 16)

    image_global_mem = cuda.to_device(image)
    compute_mandel[griddim, blockdim](-2.0, 1.0, -1.0, 1.0, image_global_mem, 20) 
    image_global_mem.copy_to_host()
    imshow(image)
    show()

