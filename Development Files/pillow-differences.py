#!/usr/bin/env python3
import sys
import PIL
from PIL import Image
from PIL import ImageChops

def compare_images(path_one, path_two, diff_save_location):
    """
    Compares to images and saves a diff image, if there
    is a difference
    
    @param: path_one: The path to the first image
    @param: path_two: The path to the second image
    """
    image1 = Image.open(path_one, mode='r')
    image2 = Image.open(path_two, mode='r')

    diff = ImageChops.difference(image1, image2).show()
    # Flag = 1 if ImageChops.difference(image1, image2).getbbox() == None else 0

    print (Flag)
    #out = abs(image1 - image2)
    
    if diff.getbbox():
        diff.save(diff_save_location)
        
if __name__ == '__main__':
    compare_images("foo-test2.jpg",
                   "foo-test3.jpg",
                   "RDC-test.jpg")



"""
Solution to make it work was to create .jpg b/c of alpha-layer issues on a png.
https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.getbbox
https://www.blog.pythonlibrary.org/2016/10/11/how-to-create-a-diff-of-an-image-in-python/
Wasn't working: bug in pillow: https://github.com/deeppomf/DeepCreamPy/issues/108#issuecomment-472964671
"""