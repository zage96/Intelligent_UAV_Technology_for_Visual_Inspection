# Stitching images together 

# This code is based upon the source code: Shawn Gomez, 19 June 2014. [Internet]. Available: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4081273/. [Accessed: 15 March 2018]



from skimage import data
from skimage import transform as tf 
from skimage.feature import (ORB, match_descriptors, corner_harris, corner_peaks, plot_matches)
from skimage.io import imread
from skimage.measure import ransac
from skimage.transform import ProjectiveTransform
from skimage.color import rgb2gray
from skimage.io import imsave, show
from skimage.color import gray2rgb
from skimage.exposure import rescale_intensity 
from skimage.transform import warp 
from skimage.transform import SimilarityTransform
import matplotlib.pyplot as plt
import numpy as np 
import cv2

from PIL import Image

import matplotlib


# Read the images 
DroneImage1 = imread('UAV_first3.jpg')
DroneImage2 = imread('UAV_second3.jpg')


# Convert the image to gray scale
DroneImage1= rgb2gray(DroneImage1)
DroneImage2= rgb2gray(DroneImage2)

# Define the number of key points and the threshold
orb = ORB(n_keypoints=1000, fast_threshold=0.5 )

# Find the key points in each picture
orb.detect_and_extract(DroneImage1)
keypointsDroneImage1 = orb.keypoints
descriptorsDroneImage1 = orb.descriptors

orb.detect_and_extract(DroneImage2)
keypointsDroneImage2 = orb.keypoints
descriptorsDroneImage2 = orb.descriptors


# Find the matching key point between the two images 
matchesImage12 = match_descriptors(descriptorsDroneImage1, descriptorsDroneImage2, cross_check=True)

# Plot the images with key points 
fig, ax = plt.subplots(nrows=2, ncols=1)
plt.gray()


plot_matches(ax[0], DroneImage1, DroneImage2, keypointsDroneImage1, keypointsDroneImage2, matchesImage12)
ax[0].axis('off')
ax[0].set_title("Left vs. Center")

plot_matches(ax[1],  DroneImage1, DroneImage2, keypointsDroneImage1, keypointsDroneImage2, matchesImage12)
ax[1].axis('off')
ax[1].set_title("Left vs. Center")


#plt.show()


src = keypointsDroneImage2[matchesImage12[:, 1]][:, ::-1 ] 
dst = keypointsDroneImage1[matchesImage12[:, 0]][:, ::-1 ] 

# Estimate the transformation model 
model_robust, inliers = \
    ransac((src, dst), ProjectiveTransform,
           min_samples=4, residual_threshold=2)

# Determine the shape of the merged image 
r, c = DroneImage2.shape[:2]
corners1 = np.array([[0, 0], [0, r], [c, 0], [c, r]])

DeformCorners = model_robust(corners1)

# Merge the arrays vertically 
CombCorners = np.vstack((DeformCorners, corners1))

MinCorner = np.min(CombCorners, axis = 0)
MaxCorner = np.max(CombCorners, axis = 0)

output_shape = (MaxCorner - MinCorner)
output_shape = np.ceil(output_shape[::-1])

offset = SimilarityTransform(translation=-MinCorner)

# Deform the image to the same size as the output_shape

DeformDroneImage1 = warp(DroneImage1, offset.inverse, output_shape=output_shape, cval=-1)
DeformDroneImage2 = warp(DroneImage2, (model_robust + offset).inverse, 
				   output_shape=output_shape, cval=-1)

# Add alpha to the find the average number of images 

MaskDroneImage1 = (DeformDroneImage1 != -1 )
DeformDroneImage1[~MaskDroneImage1] = 0
AlphaDroneImage1 = np.dstack((gray2rgb(DeformDroneImage1), MaskDroneImage1))

MaskDroneImage2 = (DeformDroneImage2 != -1 )
DeformDroneImage2[~MaskDroneImage2] = 0
AlphaDroneImage2 = np.dstack((gray2rgb(DeformDroneImage2), MaskDroneImage2))

# Merge the images together 
Merged12 = (AlphaDroneImage1 + AlphaDroneImage2)
Alpha = Merged12[..., 3]
Merged12 /= np.maximum(Alpha, 1)[..., np.newaxis]

# Save the image 
matplotlib.image.imsave('Overlapping.jpg', Merged12)



######################################################################
# Repeat the process and merge 'Overlapping.jpg' with the third photo. 
######################################################################


# Read the images 
DroneImage3 = imread('Overlapping.jpg')
DroneImage4 = imread('UAV_third2.jpg')


# Convert the image to gray scale
DroneImage3= rgb2gray(DroneImage3)
DroneImage4= rgb2gray(DroneImage4)

# Define the number of key points and the threshold
orb = ORB(n_keypoints=1000, fast_threshold=0.5 )

# Find the key points in each picture
orb.detect_and_extract(DroneImage3)
keypointsDroneImage3 = orb.keypoints
descriptorsDroneImage3 = orb.descriptors

orb.detect_and_extract(DroneImage4)
keypointsDroneImage4 = orb.keypoints
descriptorsDroneImage4 = orb.descriptors


# Find the matching key point between the two images 
matchesImage34 = match_descriptors(descriptorsDroneImage3, descriptorsDroneImage4, cross_check=True)

# Plot the images with key points 
fig, ax = plt.subplots(nrows=2, ncols=1)
plt.gray()


plot_matches(ax[0], DroneImage3, DroneImage4, keypointsDroneImage3, keypointsDroneImage4, matchesImage34)
ax[0].axis('off')
ax[0].set_title("Left vs. Center")

plot_matches(ax[1],  DroneImage3, DroneImage4, keypointsDroneImage3, keypointsDroneImage4, matchesImage34)
ax[1].axis('off')
ax[1].set_title("Left vs. Center")


#plt.show()


src = keypointsDroneImage4[matchesImage34[:, 1]][:, ::-1 ] 
dst = keypointsDroneImage3[matchesImage34[:, 0]][:, ::-1 ] 

# Estimate the transformation model 
model_robust, inliers = \
    ransac((src, dst), ProjectiveTransform,
           min_samples=4, residual_threshold=2)

# Determine the shape of the merged image 
r, c = DroneImage4.shape[:2]
corners3 = np.array([[0, 0], [0, r], [c, 0], [c, r]])

DeformCorners3 = model_robust(corners3)

# Merge the arrays vertically 
CombCorners3 = np.vstack((DeformCorners3, corners3))

MinCorner3 = np.min(CombCorners3, axis = 0)
MaxCorner3 = np.max(CombCorners3, axis = 0)

output_shape = (MaxCorner3 - MinCorner3)
output_shape = np.ceil(output_shape[::-1])

offset3 = SimilarityTransform(translation=-MinCorner3)

# Deform the image to the same size as the output_shape

DeformDroneImage3 = warp(DroneImage3, offset.inverse, output_shape=output_shape, cval=-1)
DeformDroneImage4 = warp(DroneImage4, (model_robust + offset).inverse, 
				   output_shape=output_shape, cval=-1)

# Add alpha to the find the average number of images 

MaskDroneImage3 = (DeformDroneImage3 != -1 )
DeformDroneImage3[~MaskDroneImage3] = 0
AlphaDroneImage3 = np.dstack((gray2rgb(DeformDroneImage3), MaskDroneImage3))

MaskDroneImage4 = (DeformDroneImage4 != -1 )
DeformDroneImage4[~MaskDroneImage4] = 0
AlphaDroneImage4 = np.dstack((gray2rgb(DeformDroneImage4), MaskDroneImage4))

# Merge the images together 
Merged34 = (AlphaDroneImage3 + AlphaDroneImage4)
Alpha = Merged34[..., 3]
Merged34 /= np.maximum(Alpha, 1)[..., np.newaxis]

# Save the image 
matplotlib.image.imsave('Overlapping1.jpg', Merged34)







