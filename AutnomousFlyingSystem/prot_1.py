#!/usr/bin/python

''' Program that connects to a parrot bebop drone V.1, making it fly autonomously to perform areal footage of an area. The drone flies to the marker autnomously, takes areal pictures of it and returns to another selected marker. '''

#Install the required libraries
''' Common libraries '''
import sys
import cv2
import os
import time
import signal
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import detect_color as detect

'''Bebop libraries '''
from bebop import Bebop
from commands import movePCMDCmd
from capdet import detectTwoColors, loadColors
from bebop import *
from apyros.metalog import MetaLog, disableAsserts
from apyros.manual import myKbhit, ManualControlException


import time

# Create global variables
drone = Bebop()

''' Function that provides an angle for the pitch according to tilt angle of the camera '''
def obtainSpeed(AngleCamera):      
    
    if AngleCamera == -30:
        return 20,0,False
    if AngleCamera == -42:
        return 10,-1, False
    if AngleCamera == -54:
        return 6,-2, True
    if AngleCamera == -66:
        return 5,-2, True
    return 20, 0, False


''' Function that provides an angle for the pitch according to tilt angle of the camera '''
def obtainSpeed2(AngleCamera):      
    
    if AngleCamera == -30:
        return 27,0,False
    if AngleCamera == -42:
        return 9,-3, False
    if AngleCamera == -54:
        return 5,-3, True
    if AngleCamera == -66:
        return 5,-3, True
    return 20, 0, False
        

''' Function that creates a folder called "Photos" '''
def createFolder():
    
    # Create the name of the folder's path
    file_path = "/home/bebopdev/kata/Photos/"
    directory = os.path.dirname(file_path)

    # If it does not exist, create it
    if not os.path.exists(directory):
        os.makedirs(directory)

''' Function that allows the drone to take 8 frames of a video '''
def testCamera():
    
    # Local variables
    i = 0
    
    try:
        # source of the video
        cap = cv2.VideoCapture('./bebop.sdp')
        
        # Look for 20 frames of video
        while (i < 20):
            # obtain the frame
            ret,img = cap.read()
        
            if ret: 
                # show the frame in the screen
                cv2.imshow('img', img)
                cv2.namedWindow('img', cv2.WINDOW_NORMAL)
                cv2.waitKey(1)
            # update the state of the drone
            drone.update()
            i += 1
    except (TypeError) as e:
        pass



''' Function that allows the drone to take 8 frames of a video '''
def takePict():
    
    # Local variables
    i = 0

    try:
        # source of the video
        cap = cv2.VideoCapture('./bebop.sdp')
        
        # Look for 20 frames of video
        while (i < 20):
            # obtain the frame
            ret,img = cap.read()
            
            if ret:          
                # save images from the frame 11 to above
                if (i > 11):
                    # Save the image
                    imageName = "Photo_"+ str(i) +".jpg"
                    cv2.imwrite(imageName, img)
                    
                    # obtain the coordinates of the amrker in the image
                    distancex,x,distancey=detect.coordenates(imageName)
                    distancex2 = abs(distancex)
                    
                    # Check if the marker is in the centre of X in the image
                    if distancex2 < 80:
                        # Print status messages
                        print 'Object Centred'
                        print 'x: ', distancex, 'y :', distancey
                        
                        # Move the image to the folder
                        current_path = "Photo_"+ str(i) +".jpg"
                        final_path = "Photos/" + current_path
                        os.rename(current_path, final_path)
                        # Say that the marker is centred and return the coordinates
                        i = 20
                        return True, distancex, distancey
            # update the state of the drone
            drone.update()
            i += 1
        # Say that the marker is NOT centred and return the coordinates
        return False, distancex, distancey
    except (TypeError) as e:
        pass

''' Function that helps to find a target '''
def findTarget(angleCamera):
    
    # Local variables
    centred =  False
    YawAngle = 15
    
    
    while not centred : 
        # Obtain the images
        centred, xvalue, yvalue = takePict()
        
        if not centred :         
            # modify the angle to Yaw
            if xvalue < 0:
                # Print status messages
                print "Rotating left"
                
                YawAngle = -16
                RollAngle = -7
            else :
                # Print status messages
                print "Rotating right"
                
                YawAngle = 16
                RollAngle = 7
            if yvalue > 0:
                pitch = 11
            else:
                pitch = 5
            # Make the drone Yaw
            # This compensate the movement to the back of the drone
            drone.moveBebop(0, 1, 0)
            drone.wait(1)
            
            # Rotate(Yaw)
            drone.moveBebop(0, pitch-3, YawAngle)  
            drone.wait(1)
            drone.moveBebop(RollAngle,pitch-1,0)
            drone.wait(1)
            
            # This compensate the movement to the back of the drone
            drone.moveBebop(0, 1, 0)


    # Check the position in Y to tilt the camera  
    if yvalue < -30:
        if angleCamera > -80:
            angleCamera = angleCamera - 12
    
    # Print status messages
    print "Angle Camera :", angleCamera
    
    return angleCamera, xvalue,yvalue

''' function to arrive to target'''
def arrive():
    # Local varaibles
    angleCamera = -30
    there = False
    
    while not there:
        # Find and centre the target
        NewangeleCamera,x,y = findTarget(angleCamera)
        angleCamera = NewangeleCamera
        
        # Tilt the camera
        drone.moveCamera(tilt=angleCamera, pan=0)

        # Print status messages
        print "Moving forward"
        
        # This compensate the movement to the back of the drone
        drone.moveBebop(0, 1, 0)
        drone.wait(1)

        # Obtain the angle for the roll movement
        speed,counter,there =obtainSpeed(angleCamera)      
      
        # Print status messages
        print 'Pitch :', speed, ' Counter: ',counter
        
        if x > 0:
            Roll = 7
        else:
            Roll = -7

        # Make the pitch movement
        drone.moveBebop(Roll, speed, 0)
        drone.wait(1)
        drone.moveBebop(0, counter, 0) 
        drone.wait(1)
        
        # This compensate the movement to the back of the drone
        drone.moveBebop(0, 1, 0)
        
        # Emergency break, in case of moving to much forward
        if angleCamera >= -42 and y < -120 :
            print ' Emergency stop '
            there = True
            # Stop the bebop
            drone.moveBebop(0, -5, 0)
            drone.wait(1)

''' Function that allows the drone to take 8 frames of a video '''
def UAVPict(Position):

    # Local variables
    i = 0

    try:
        # source of the video
        cap = cv2.VideoCapture('./bebop.sdp')
        
        # Look for 20 frames of video
        while (i < 20):
            # obtain the frame
            ret,img = cap.read()
            
            if ret: 
                # save images from the frame 11 to above
                if (i > 11):
                    # Save the image
                    imageName = "UAV_"+ Position + str(i - 11) +".jpg"
                    cv2.imwrite(imageName, img)
                    
                    # Print status messages
                    print 'Photo taken : ', Position
                    
                    # Move the image to the folder
                    current_path = imageName
                    final_path = "Photos/" + current_path
                    os.rename(current_path, final_path)

            # update the state of the drone
            drone.update()
            i += 1
    except (TypeError) as e:
        pass


''' Function that makes the drone hover over the target and take pictures '''
def AerealFootage():
    
    # Adjust the camera 
    drone.moveCamera(tilt= -90, pan=0)
    
    # Hover
    drone.moveBebop(-1, 0, 0) 
    drone.moveBebop(1, 0, 0)
    drone.moveBebop(0, 1, 0)
    
     # Take the pictures centre
    UAVPict("First")
    
    # Setting Yaw, Roll and Pitch values
    YawAngle = 30
    RollAngle = 9
    pitch = 9

    # Rotate
    drone.moveBebop(0, 1, 0)
    drone.wait(1)
    drone.moveBebop(0, 4, YawAngle)  
    drone.wait(2)
    drone.moveBebop(RollAngle,pitch,0)
    drone.wait(1)
    drone.moveBebop(0, 1, 0)

    # Take the pictures centre
    UAVPict("Second")

    # Setting Yaw, Roll and Pitch values
    YawAngle = 30
    RollAngle = 9
    pitch = 12

    # Rotate
    drone.moveBebop(0, 1, 0)
    drone.wait(1)
    drone.moveBebop(0, pitch, YawAngle)  
    drone.wait(2)
    drone.moveBebop(RollAngle,pitch+1,0)
    drone.wait(2)
    
    # Take the pictures centre
    UAVPict("Third")    


''' Function that place the drone in a better position to the take the UAV photos '''
def accomodate():

     # take the pictures
    drone.moveBebop(0, 1, 0)
    centred, xvalue, yvalue = takePict()
        
    if not centred :
        
        # modify the Yaw value
        if xvalue < 0:
            # Print status messages
            print "Rotating left"
            
            YawAngle = -15
            RollAngle = -7
        else :
            # Print status messages
            print "Rotating right"
            
            YawAngle = 15
            RollAngle = 7

        # Obtain the pitch value
        if yvalue > 0:
            pitch = 9
        else:
            pitch = 5

        # Rotate
        drone.moveBebop(0, pitch, YawAngle)  
        drone.wait(1)
        drone.moveBebop(RollAngle,pitch,0)
        drone.wait(1)
    
    # Make the drone fly to 1.5 m of altitude
    drone.hover()    
    drone.flyToAltitude(1.5)
    drone.flyToAltitude(1.5)
    
    # Make the drone Yaw
    # This compensate the movement to the back of the drone
    drone.moveBebop(0, 1, 0)

''' function to arrive to the second target'''
def arrive2():

    # Local varaibles
    angleCamera = -30
    there = False
    
    while not there:
        # Find and centre the target
        NewangeleCamera,x,y = findTarget(angleCamera)
        angleCamera = NewangeleCamera
        
        # Tilt the camera
        drone.moveCamera(tilt=angleCamera, pan=0)

        # Print status messages
        print "Moving forward"
        
        # This compensate the movement to the back of the drone
        drone.moveBebop(-1, 1, 0)
        drone.wait(1)

        # Obtain the angle for the roll movement
        speed,counter,there =obtainSpeed2(angleCamera)      
      
        # Print status messages
        print 'Pitch :', speed, ' Counter: ',counter

        # Obtain some roll values for compensation
        if x > 0:
            Roll = 7
        else:
            Roll = -7

        # Make the pitch movement
        drone.moveBebop(Roll, speed, 0)
        drone.wait(1)
        drone.moveBebop(-1, counter, 0) 
        drone.wait(1)
        
        # This compensate the movement to the back of the drone
        drone.moveBebop(-1, 1, 0)


''' Make the drone return the initial position (with a marker) '''
def comeBack():

    # Tilt the camera to -30 
    drone.moveCamera(tilt= -30, pan=0)

    # Rotate the drone one more time
    YawAngle = 25
    RollAngle = -17
    pitch = 15

    # Rotate
    drone.moveBebop(0, 1, 0)
    drone.wait(1)
    drone.moveBebop(-5, 10, YawAngle)  
    drone.wait(3)
    drone.moveBebop(RollAngle,pitch,0)
    drone.wait(2)

    # Make it fly to 1.8 meters
    drone.flyToAltitude(1.8) 
    drone.moveBebop(-5, 10, 0) 
    drone.wait(2)

    # Make it come back
    drone.moveBebop(-2, 5, 0) 
    drone.wait(2)
    arrive2()
    
    
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
    drone.takeoff()
    drone.flyToAltitude(1.8) 
    drone.moveBebop(0, 5, 0) 
    drone.flyToAltitude(1.8)      
    drone.moveBebop(0, 7, 0) 
    drone.wait(2)

    # look for the target and arrive there
    arrive()    
    
    # Accomodate the drone before taking picures
    accomodate()

    # Take the Areal pictures
    AerealFootage()    
    
    # Return
    comeBack()
       
    # finish all the operations
    drone.land()
    sys.exit(0)
    

''' Detects when the prgram has been interrupted'''
def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    drone.land()
    sys.exit(0)

if __name__ == "__main__":
    print "Battery:", drone.battery
    if (drone.battery > 2) :
        main()
    else :
        print "Battery too low"
