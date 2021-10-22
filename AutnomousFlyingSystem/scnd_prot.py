#!/usr/bin/python
import sys
import cv2
import os
import time
import signal
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import detect_color as detect

'''Bebop libraries'''
from bebop import Bebop
from commands import movePCMDCmd
from capdet import detectTwoColors, loadColors
from bebop import *
# this will be in new separate repository as common library fo robotika Python-powered robots
from apyros.metalog import MetaLog, disableAsserts
from apyros.manual import myKbhit, ManualControlException

import time


drone = Bebop()

        
''' Function that creates a folder called "Photos" '''
def createFolder():
    file_path = "/home/bebopdev/kata/Photos/"
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

''' Function that allows the drone to take 8 frames of a video '''
def testCamera():
    # Local variables
    i = 0
    # signal.signal(signal.SIGINT, signal_handler)
    try:
        cap = cv2.VideoCapture('./bebop.sdp')
        
        # Look for 20 frames
        while (i < 20):
            ret,img = cap.read()
            if ret: 
                cv2.imshow('img', img)
                cv2.namedWindow('img', cv2.WINDOW_NORMAL)
                cv2.waitKey(1)
            drone.update()
            i += 1
    except (TypeError) as e:
        pass


''' Function that allows the drone to take 8 frames of a video '''
def takePict():
    # Local variables
    i = 0
    # signal.signal(signal.SIGINT, signal_handler)
    try:
        cap = cv2.VideoCapture('./bebop.sdp')
        
        # Look for 20 frames
        while (i < 20):
            ret,img = cap.read()
            if ret: 
                cv2.imshow('img', img)
                cv2.namedWindow('img', cv2.WINDOW_NORMAL)
                cv2.waitKey(1)
                # save images from the frame 11 to above
                if (i > 11):
                    # Save the image
                    LenameImg = "Photo_"+ str(i) +".jpg"
                    cv2.imwrite(LenameImg, img)
                    distancex,x,distancey=detect.coordenates(LenameImg)
                    distancex2 = abs(distancex)
                    # Check if the point is in the centre of the image
                    if distancex2 < 50:
                        print 'Found!########################################'
                        print 'x: ', distancex, 'y :', distancey
                        # Move the image to the folder
                        current_path = "Photo_"+ str(i) +".jpg"
                        final_path = "Photos/" + current_path
                        os.rename(current_path, final_path)
                        return True, distancex, distancey

            drone.update()
            i += 1
        return False, distancex, distancey
    except (TypeError) as e:
        pass

''' Function that helps to find a target '''
def findTarget(angleCamera):

    found =  False
    YawAngle = 23
    
    while not found : 
        # Obtain the images
        found, xvalue, yvalue = takePict()
        
        if not found :
            # modify the angle to Yaw
            if xvalue < 0:
                print "Moving Right!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                YawAngle = -13
            else :
                print "Moving LEFT@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
                YawAngle = 13
            # Make the drone Yaw
            drone.hover()
            drone.wait(1)
            drone.moveBebop(0, 0, YawAngle)  
            drone.wait(1) 
            drone.hover()
            
            # Adjust the camera
            drone.moveCamera(tilt=angleCamera, pan=0)
            #drone.flyToAltitude(1.5)
            print "Angle Camera :", angleCamera
    print "Angle Camera :", angleCamera
    #if yvalue > 30:
    #    if angleCamera < 70:
    #        angleCamera = angleCamera + 20
    if yvalue < -30:
        if angleCamera > -70:
            angleCamera = angleCamera - 20
    else:
        angleCamera = angleCamera
    #drone.moveCamera(tilt=angleCamera, pan=0)
    return angleCamera
            
''' function to arrive to target'''
def arrive():
    angleCamera = -70
    centered = False
    while not centered:
        NewangeleCamera = findTarget(angleCamera)
        angleCamera = NewangeleCamera
        drone.moveCamera(tilt=angleCamera, pan=0)
        #if angleCamera > -70:
        print "MOOOOOOOOOOOOOOOVVVVVVVVVVVVVVIIIIIIIIIIIIINNNNNNNNNNNGGGGGGGGGGG"
        drone.hover()
        drone.wait(1)            
        drone.moveBebop(0, 13, 0) 
        drone.wait(1)
        drone.moveBebop(0, -5, 0) 
        drone.wait(1)
        drone.hover()
            #drone.flyToAltitude(1.5)

    
'''Main function '''
def main():
    # We create the folder for the images
    createFolder()
    
    # Prepare the camera
    # Establish the signal of the camera with the computer
    signal.signal(signal.SIGINT, signal_handler)
    
    # adjust the camera for the video
    drone.moveCamera(tilt= -30, pan=0)
    
    # Start the video
    drone.videoEnable()
    testCamera()

    # take off
    #drone.wait(2)
    drone.takeoff()
    drone.flyToAltitude(2)    

    # look for the target
    #angleCamera = -30
    #NewangeleCamera = findTarget(angleCamera)
    arrive()    
    
    # fly there
    
        
    
    # finish all the operations
    drone.land()
    sys.exit(0)
    

''' Detects when the prgram has been interrupted'''
def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    #drone.land()
    sys.exit(0)

if __name__ == "__main__":
    print "Battery:", drone.battery
    if (drone.battery > 2) :
        main()
    else :
        print "Battery too low"
