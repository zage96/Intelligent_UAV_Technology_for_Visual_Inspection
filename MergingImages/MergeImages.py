


# Merging images horizontally.

# This code is based upon the source code: min2bro, 12 July 2017 . [Internet]. Available: https://kanoki.org/2017/07/12/merge-images-with-python/. [Accessed: 14 March 2018]



import numpy as np
import cv2
import sys
import os
import operator 


from PIL import Image
from PIL import ImageDraw



# Load the images
DroneImages = ['UAV_first3.jpg', 'UAV_second3.jpg', 'UAV_third2.jpg']
DroneImg = [ Image.open(i) for i in DroneImages ]

# Resize the images to match the size of the smallest image 
MinDroneImageShape = sorted( [(np.sum(i.size), i.size ) for i in DroneImg])[0][1]

# Merge the images horizontally
DroneImageMerge = np.hstack( (np.asarray( i.resize(MinDroneImageShape,Image.ANTIALIAS) ) for i in DroneImg) )

# Creating an image memory 
DroneImageMerge = Image.fromarray(DroneImageMerge)

# Save the image
DroneImageMerge.save( 'MergeImages.jpg' )

# Plot the image 
DroneImageMerge.show()



