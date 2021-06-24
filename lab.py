#!/usr/bin/env python3

import math
from PIL import Image as Image

# NO ADDITIONAL IMPORTS ALLOWED!




def get_pixel(image, x, y):
    #store height and width as values
    height = image['height']
    width = image['width']
    #accounts for edge cases
    if y > height - 1:
        y = height - 1
    if y < 0:
        y=0
    if x > width - 1:
        x = width - 1
    if x < 0:
        x = 0 
    #calculation to turn list index into matrix index
    index = (width*y)+x
    return image['pixels'][index]

i = {'height': 3, 'width': 2, 'pixels': [0, 50, 50, 100, 100, 255]}

print(get_pixel(i, 2, 2))

def set_pixel(image, x, y, c):
    #store height and width as values
    height = image['height']
    width = image['width']
    #account for edge cases 
    if y > height - 1:
        y = height - 1
    if y < 0:
        y=0
    if x > width - 1:
        x = width - 1
    if x < 0:
        x = 0 
    #calculation to turn list index into matrix index
    index = (width*y)+x
    image['pixels'][index] = c

def apply_per_pixel(image, func):
    #initialize image made of zeros
    result = {
        'height': image['height'],
        'width': image['width'],
        'pixels': len(image['pixels'])*[0],
    }
    #apply new color to each combination of pixels
    for x in range(image['width']):
        for y in range(image['height']):
            color = get_pixel(image, x, y)
            newcolor = func(color)
            set_pixel(result, x, y, newcolor)
    return result


def inverted(image):
    #should be 256, not 255
    return apply_per_pixel(image, lambda c: 255-c)



def correlate(image, kernel):
    """
    Compute the result of correlating the given image with the given kernel.

    The output of this function should have the same form as a 6.009 image (a
    dictionary with 'height', 'width', and 'pixels' keys), but its pixel values
    do not necessarily need to be in the range [0,255], nor do they need to be
    integers (they should not be clipped or rounded at all).

    This process should not mutate the input image; rather, it should create a
    separate structure to represent the output.

    Representing kernel as a dictionary
    """
    #store the width, height, and kernel dimension
    #store initialized image
    image_width = image['width']
    image_height = image['height']
    kernel_width = kernel['width']
    kernel_height = kernel['height']
    kernel_dimension = kernel['width']//2
    new_image = {'height': image['height'], 'width': image['width'], 'pixels': len(image['pixels'])*[0]}
    
    #loop through every coord
    for x in range(image_width):
        for y in range(image_height):
            #initialize total sum
            total = 0 
            #loop through every coord in the kernel
            for y_kernel in range(kernel_width):
                for x_kernel in range(kernel_height):
                    #calculation for new x and y 
                    result_x = x-kernel_dimension+x_kernel
                    result_y = y-kernel_dimension+y_kernel
                    #add to total
                    result_val = get_pixel(image, result_x, result_y)*get_pixel(kernel, x_kernel, y_kernel)
                    total += result_val
                #set new pixel value and return new image
            set_pixel(new_image, x, y, total)
    return new_image


def round_and_clip_image(image):
    """
    Given a dictionary, ensure that the values in the 'pixels' list are all
    integers in the range [0, 255].

    All values should be converted to integers using Python's `round` function.

    Any locations with values higher than 255 in the input should have value
    255 in the output; and any locations with values lower than 0 in the input
    should have value 0 in the output.
    """
    #initialize an image of all zeros
    new_image = {'height': image['height'], 'width': image['width'], 'pixels': image['pixels'].copy()}
    len_pixels = len(new_image['pixels'])
    #perform calculations to round and clip image
    for i in range(len_pixels):
        new_image['pixels'][i] = int(round(new_image['pixels'][i]))
        if new_image['pixels'][i] > 255:
            new_image['pixels'][i] = 255
        if new_image['pixels'][i] < 0:
            new_image['pixels'][i] = 0 
    return new_image
        

def make_matrix(n):
    """
    Given an input n, returns a blur box for use in the Blurred Image function
    
    """
    #number that makes up the matrix depending on value of n
    num = 1/n**2
    #creates a blur box as a dictionary
    blur_box = {'height': n, 'width': n, 'pixels': [num]*n**2 }
    return blur_box 
    
def blurred(image, n):
    """
    Return a new image representing the result of applying a box blur (with
    kernel size n) to the given input image.

    This process should not mutate the input image; rather, it should create a
    separate structure to represent the output.
    """
    #access the relvant blur box and then correlates with new image
    blur_box = make_matrix(n)
    new_image = correlate(image, blur_box)
    return round_and_clip_image(new_image)


# HELPER FUNCTIONS FOR LOADING AND SAVING IMAGES
    
def sharpened(image, n):
    """
    Returns a new sharpened image using relevant calculation of subtracting blurred image.
    
    This process should not mutate the input image; rather returns a new one.
    
    """
    #store image width and height
    image_width = image['width']
    image_height = image['height']
    #intialize new image and stores blurred image
    new_image = {'height': image['height'], 'width': image['width'], 'pixels': len(image['pixels'])*[0]}
    blurred_image = blurred(image, n)
    
    #loop through every coordinate
    for x in range(image_width):
        for y in range(image_height):
            #perform calculation and set pixel
            a = 2*get_pixel(image, x, y) - get_pixel(blurred_image, x, y)
            set_pixel(new_image, x, y, a)
    return round_and_clip_image(new_image)

def edges(image):
    """
    Impletments a filter which detects the edges of an image with the Sobel Operator.
    
    Does not modify the input image; rather, it returns a new image.
    
    """
    #store image width and height and initialize new image
    image_width = image['width']
    image_height = image['height']
    new_image = {'height': image['height'], 'width': image['width'], 'pixels': len(image['pixels'])*[0]}
    
    #sobel operator kernels
    kernel_x = {'height': 3, 'width': 3, 'pixels': [-1,0,1,-2,0,2,-1,0,1]}
    kernel_y = {'height': 3, 'width': 3, 'pixels': [-1,-2,-1,0,0,0,1,2,1]}
    
    #creating the filters
    o_x = correlate(image, kernel_x)
    o_y = correlate(image, kernel_y)

    #perform relvant calculation for each pixel 
    for x in range(image_width):
        for y in range(image_height):
            a = ((get_pixel(o_x, x, y))**2+(get_pixel(o_y, x, y))**2)**0.5
            set_pixel(new_image, x, y, a)
    return round_and_clip_image(new_image)
    
            

def load_image(filename):
    """
    Loads an image from the given file and returns a dictionary
    representing that image.  This also performs conversion to greyscale.

    Invoked as, for example:
       i = load_image('test_images/cat.png')
    """
    with open(filename, 'rb') as img_handle:
        img = Image.open(img_handle)
        img_data = img.getdata()
        if img.mode.startswith('RGB'):
            pixels = [round(.299 * p[0] + .587 * p[1] + .114 * p[2])
                      for p in img_data]
        elif img.mode == 'LA':
            pixels = [p[0] for p in img_data]
        elif img.mode == 'L':
            pixels = list(img_data)
        else:
            raise ValueError('Unsupported image mode: %r' % img.mode)
        w, h = img.size
        return {'height': h, 'width': w, 'pixels': pixels}


def save_image(image, filename, mode='PNG'):
    """
    Saves the given image to disk or to a file-like object.  If filename is
    given as a string, the file type will be inferred from the given name.  If
    filename is given as a file-like object, the file type will be determined
    by the 'mode' parameter.
    """
    out = Image.new(mode='L', size=(image['width'], image['height']))
    out.putdata(image['pixels'])
    if isinstance(filename, str):
        out.save(filename)
    else:
        out.save(filename, mode)
    out.close()




if __name__ == '__main__':
    #pass
    # code in this block will only be run when you explicitly run your script,
    # and not when the tests are being run.  this is a good place for
    # generating images, etc.
#    l = [0]*81
#    l[18] = 1
#    kernel = {'height': 9, 'width': 9, 'pixels': l}
     im = load_image('test_images/construct.png')
#    
     new_image = edges(im)
     save_image(new_image, 'test_construct.png')
  
    
        
    
    


