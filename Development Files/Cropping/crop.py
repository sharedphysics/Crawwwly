#!/usr/bin/python3

import os
from os import listdir
import PIL
from PIL import Image
from PIL import ImageChops


# Opens a image in RGB mode 
im = Image.open(r"test-original.jpg") 
  
# Size of the image in pixels (size of orginal image) 
# (This is not mandatory) 
width, height = im.size 
  
# Setting the points for cropped image 
left = 0
top = 0
right = width
bottom = 1440
  
# Cropped image of above dimension 
# (It will not change orginal image) 
im1 = im.crop((left, top, right, bottom)) 
  
# Shows the image in image viewer 
im1.show() 

"""
NOTES:

- https://www.geeksforgeeks.org/python-pil-image-crop-method/

"""