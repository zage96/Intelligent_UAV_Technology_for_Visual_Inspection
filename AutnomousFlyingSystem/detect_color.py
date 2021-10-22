# import the necessary packages
import time
import cv2
import numpy as np
from PIL import Image

''' Program that receives an image and detects the coordantes of an specifiec color object '''

def coordenates(name):
    # Read the image    
    image = cv2.imread(name)
    
    # Blur the image
    blur = cv2.blur(image, (3,3))

    # Select the lower and upper boundaries
    lower = np.array([76,31,4],dtype="uint8")
    upper = np.array([210,90,70], dtype="uint8")

    # Apply the threhold to the blurred image
    thresh = cv2.inRange(blur, lower, upper)
    thresh2 = thresh.copy()

    # find contours in the threshold image
    image, contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

    # finding contour with maximum area and store it as best_cnt
    max_area = 0
    best_cnt = 1
    for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > max_area:
                    max_area = area
                    best_cnt = cnt

    # finding centroids of best_cnt and draw a circle there
    M = cv2.moments(best_cnt)
    cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])

    # Modify the values to show them
    im = Image.open(name)
    width, height = im.size #size of our image
    distance= (cx-width/2)

    #print(distance)# if positive the object is on the right side of the image 
    b=((height/2) - cy)
    
    if((height/2) >= cy):
       x=1 # object in the upper part of the image
    else:
       x=0 #object in the lower part of the image

    return distance,x,b 


