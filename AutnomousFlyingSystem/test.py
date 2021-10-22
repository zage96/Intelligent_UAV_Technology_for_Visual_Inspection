#!/usr/bin/python
"""
  ARDrone3 demo with autonomous navigation to two color Parrot Cap
  usage:
       ./demo.py <task> [<metalog> [<F>]]
"""
#!/usr/bin/python
import sys
import cv2
import os
import time
import signal
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import mycode as my

from bebop import Bebop
from commands import movePCMDCmd
from capdet import detectTwoColors, loadColors
from bebop import *
# this will be in new separate repository as common library fo robotika Python-powered robots
from apyros.metalog import MetaLog, disableAsserts
from apyros.manual import myKbhit, ManualControlException

import time


drone = Bebop()
#drone.land()

################################################################
"""
''' Fly while streaming video and move the camera'''
def main():
    print "Starting"
    print "Battery:", drone.battery
    if (drone.battery > 50) :
        drone.trim()
        drone.takeoff()
        drone.flyToAltitude(1)
        tiltvalue = -50
        counter = 0
        signal.signal(signal.SIGINT, signal_handler)
        try:
            drone.moveCamera(tilt=tiltvalue, pan=0)
            drone.videoEnable()
    
            cap = cv2.VideoCapture('./bebop.sdp')
            i = 0
            while counter < 5:
                ret, img = cap.read()
                #nameImg = "/home/bebopdev/kata/Photo_"+i+".png"
                #imwrite( nameImg, img )
                if ret:
                    cv2.imshow('img', img)
                    cv2.namedWindow('img', cv2.WINDOW_NORMAL)
                    cv2.waitKey(1)
                #drone.wait(1)
                i += 1
                if i > 100:
                    tiltvalue += 10
                    drone.moveCamera(tilt=tiltvalue, pan=0)
                    i = 0
                    counter +=1
                drone.update()
            #drone.land()
            sys.exit(0)
        except (TypeError) as e:
            pass
    else :
        sys.exit(0)

def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    drone.land()
    sys.exit(0)

if __name__ == "__main__":
    main()
"""

############################################################################
"""
''' testFlying'''

print "Starting"
print "Battery:", drone.battery
testFlying(drone)
"""
############################################################################
"""
'''
store images from different frames of a video
'''

def main(): 
    i = 0
    signal.signal(signal.SIGINT, signal_handler)
    try:
        drone.moveCamera(tilt=0, pan=0)
        drone.videoEnable()
        
        cap = cv2.VideoCapture('./bebop.sdp')
        #drone.wait(2)
        while (i<20):
            ret,img = cap.read()
            if ret: 
                if (i > 10):
                    LenameImg = "Photo_"+ str(i) +".jpg"
                    
                    cv2.imwrite(LenameImg, img)
                    distancex,x,distancey=my.mycode(LenameImg)
            drone.update()
            i += 1
        sys.exit(0)
    except (TypeError) as e:
        pass

def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)

if __name__ == "__main__":
    main()

"""
############################################################################
"""
''' test to create a folder'''
def main(): 
    file_path = "/home/bebopdev/kata/Photos"
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

if __name__ == "__main__":
    main()
"""
############################################################################

"""
'''test on keyboard inputs'''
def main():    
    print "Starting"
    print "Battery:", drone.battery
    if (drone.battery > 50) :
        save = raw_input("if in problems write . s .")
        if (save == "s"):
            
            sys.exit(0)
        else:
            drone.takeoff()
            #drone.land()

        save = raw_input("if in problems write . s .")
        if (save == "s"):
            drone.land()
            sys.exit(0)     
        else:
            drone.flyToAltitude(1)
        save = raw_input("if in problems write . s .")
        if (save == "s"):
            drone.land()
            sys.exit(0)
            
        else:
            drone.rotate(30)
        save = raw_input("if in problems write . s .")
        if (save == "s"):
            drone.land()
            sys.exit(0)
            
        else:
            drone.wait(5)
        save = raw_input("if in problems write . s .")
        if (save == "s"):
            drone.land()
            sys.exit(0)
            
        else:
            drone.land()
        sys.exit(0)    

def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    #drone.land()
    sys.exit(0)

if __name__ == "__main__":
    main()
"""
############################################################################

"""
'''test on keyboard interrupt'''
def main():    
    print "Starting"
    print "Battery:", drone.battery
    if (drone.battery > 50) :
        drone.takeoff()
        drone.flyToAltitude(2)
        while True:      
            drone.hover()  
            drone.moveBebop(-1, 0, 0) 
            #drone.wait(1)
            drone.moveBebop(1, 0, 0)
            #drone.wait(1)
        drone.land()
        sys.exit(0) 
            #drone.takeoff()
            #drone.land()
            #drone.flyToAltitude(1)
            #drone.rotate(30)
            #drone.wait(5)
   

def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    #drone.land()
    sys.exit(0)

if __name__ == "__main__":
    main()
"""



###########################################################################
"""
''' test on atexit interrupt'''
def saveMe():
    drone.land()
    sys.exit(0)	

import atexit
atexit.register(saveMe)
"""

#######################################################################

"""

''' Test to make the drone move forward (PITCH)'''


def main():    
    print "Starting"
    print "Battery:", drone.battery
    if (drone.battery > 2) :
        drone.takeoff()
        drone.flyToAltitude(1)
        drone.hover()
        drone.moveBebop(0,7,0) 
        drone.wait(2)
        drone.hover()
        drone.land()
        sys.exit(0)    

def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)

if __name__ == "__main__":
    main()


"""
#####################################################################
"""
''' see what is the maximun angle of the camera'''
def main():
    print "Starting"
    print "Battery:", drone.battery
    if (drone.battery > 1) :
        tiltvalue = 0
        counter = 0
        signal.signal(signal.SIGINT, signal_handler)
        try:
            drone.moveCamera(tilt=tiltvalue, pan=0)
            drone.videoEnable()
    
            cap = cv2.VideoCapture('./bebop.sdp')
            i = 0
            while counter < 10:
                ret, img = cap.read()
                if ret:
                    cv2.imshow('img', img)
                    cv2.namedWindow('img', cv2.WINDOW_NORMAL)
                    cv2.waitKey(1)
                #drone.wait(1)
                i += 1
                if i > 100:
                    if tiltvalue < 100:
                        tiltvalue -= 10
                    drone.moveCamera(tilt=tiltvalue, pan=0)
                    i = 0
                    counter +=1
                drone.update()
            sys.exit(0)
        except (TypeError) as e:
            pass
    else :
        sys.exit(0)

def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    drone.land()
    sys.exit(0)

if __name__ == "__main__":
    main()
"""
#####################################################################

"""
''' obtain different points of the camera'''
def main():
    print "Starting"
    print "Battery:", drone.battery
    if (drone.battery > 1) :
        tiltvalue = -30
        counter = 0
        signal.signal(signal.SIGINT, signal_handler)
        try:
            drone.moveCamera(tilt=tiltvalue, pan=0)
            drone.videoEnable()
    
            cap = cv2.VideoCapture('./bebop.sdp')
            i = 0
            while i < 100:
                ret, img = cap.read()
                if ret:
                    cv2.imshow('img', img)
                    cv2.namedWindow('img', cv2.WINDOW_NORMAL)
                    cv2.waitKey(1)
                i += 1
                if i > 99:
                    tiltvalue = -45
                    print ""
                    print ""
                    print ""
                    print ""
                    print ""
                    print "tilt : ", tiltvalue, "#################################################"
                    print ""
                    print ""
                    print ""
                    print ""
                    print ""
                    drone.moveCamera(tilt=tiltvalue, pan=0)
                    #i = 0
                    counter +=1
                drone.update()
            i = 0
            while i < 100:
                ret, img = cap.read()
                if ret:
                    cv2.imshow('img', img)
                    cv2.namedWindow('img', cv2.WINDOW_NORMAL)
                    cv2.waitKey(1)
                i += 1
                if i > 99:
                    tiltvalue = -70
                    print ""
                    print ""
                    print ""
                    print ""
                    print ""
                    print "tilt : ", tiltvalue, "#################################################"
                    print ""
                    print ""
                    print ""
                    print ""
                    print ""
                    drone.moveCamera(tilt=tiltvalue, pan=0)
                    #i = 0
                    counter +=1
                drone.update()    
            i = 0
            while i < 100:
                ret, img = cap.read()
                if ret:
                    cv2.imshow('img', img)
                    cv2.namedWindow('img', cv2.WINDOW_NORMAL)
                    cv2.waitKey(1)
                i += 1
                if i > 99:
                    #tiltvalue = -45
                    print ""
                    print ""
                    print ""
                    print ""
                    print ""
                    #print "tilt : ", tiltvalue, "#################################################"
                    print ""
                    print ""
                    print ""
                    print ""
                    print ""
                    #drone.moveCamera(tilt=tiltvalue, pan=0)
                    #i = 0
                    counter +=1
                drone.update()
            sys.exit(0)
        except (TypeError) as e:
            pass
    else :
        sys.exit(0)

def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    drone.land()
    sys.exit(0)

if __name__ == "__main__":
    main()

"""

#####################################################################
"""
'''test on making hovering better'''
def main():    
    print "Starting"
    print "Battery:", drone.battery
    if (drone.battery > 1) :
        drone.takeoff()
        drone.flyToAltitude(2)
        while True:      
            drone.hover()  
            #drone.moveBebop(-2, 0, 0) 
            #drone.moveBebop(1, 0, 0)
        drone.land()
        sys.exit(0) 
            #drone.takeoff()
            #drone.land()
            #drone.flyToAltitude(1)
            #drone.rotate(30)
            #drone.wait(5)
   

def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    drone.land()
    sys.exit(0)

if __name__ == "__main__":
    main()
"""

####################################################################

'''test photo quality'''
def main():    
    print "Starting"
    print "Battery:", drone.battery
    if (drone.battery > 1) :
        signal.signal(signal.SIGINT, signal_handler)
        try:
            drone.moveCamera(tilt=0, pan=0)
            drone.videoEnable()
    
            cap = cv2.VideoCapture('./bebop.sdp')
            drone.takePicture()
            #drone.wait(1)
            drone.takePicture()
        except (TypeError) as e:
            pass
        sys.exit(0) 

   

def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    #drone.land()
    sys.exit(0)

if __name__ == "__main__":
    main()


####################################################################

"""
''' Function that makes the drone hover over the target and take pictures '''
def AerealFootage():
    
    # Adjust the camera 
    drone.moveCamera(tilt= -80, pan=0)
    
    # go to the positio to take pictures    
    drone.flyToAltitude(1.5)

    
    centred, x, y = takePict()
    if y > 100:
        pitch = 15
        contrarest = -3
    elif y < 100:
        pitch = 5
        contrarest = -1
    else:
        pitch = 0
        contrarest = 0
    print 'Vertical adjustments', y, pitch,'##########################'
    if pitch != 0:  
        # move a little forward
        drone.moveBebop(0, pitch, 0) 
        drone.wait(1)
        drone.moveBebop(0, contrarest, 0) 
        drone.wait(1)
        drone.hover()
    
    # This compensate the movement to the right of the drone
    drone.moveBebop(-1, 0, 0) 
    drone.moveBebop(1, 0, 0)
    drone.hover()    
    
    centred, x, y = takePict()
    if x > 150:
        Roll = 15
        contrarest = -3
    elif x < 150:
        Roll = 0
        contrarest = 0
    else:
        Roll = 10
        contrarest = -2
    if y > 100:
        pitch = 15
        pcontrarest = -3
    elif y < 100:
        pitch = 5
        pcontrarest = -1
    else:
        pitch = 0
        pcontrarest = 0
    
    print 'Vertical adjustments', y, pitch,'##########################'
    print 'Horizontal adjustments', x, Roll,'##########################'
    if Roll != 0:
        # Move to the right
        drone.moveBebop(Roll, pitch, 0) 
        drone.wait(2)
        drone.moveBebop(contrarest, pcontrarest, 0) 
        drone.wait(1)
    
    # Hover
    drone.moveBebop(-1, 0, 0) 
    drone.moveBebop(1, 0, 0)
    drone.hover()
    
    # Take the pictures
    UAVPict("Right")
    
    centred, x, y = takePict()
    if x > 150:
        Roll = 10
        contrarest = -2
    elif x < 150:
        Roll = -10
        contrarest = 2
    else:
        Roll = 0
        contrarest = 0
    if y > 100:
        pitch = 15
        pcontrarest = -3
    elif y < 100:
        pitch = 5
        pcontrarest = -1
    else:
        pitch = 0
        pcontrarest = 0
    print 'Vertical adjustments', y, pitch,'##########################'
    print 'Horizontal adjustments', x, Roll,'##########################'
    if Roll != 0:
        # Move to the Centre
        drone.moveBebop(Roll, pitch, 0) 
        drone.wait(2)
        drone.moveBebop(contrarest, pcontrarest, 0) 
        drone.wait(1)
    
    # Hover
    drone.moveBebop(-1, 0, 0) 
    drone.moveBebop(1, 0, 0)
    drone.hover()
    
    
    # Take the pictures
    UAVPict("Centre")


    centred, x, y = takePict()
    if x > 150:
        Roll = 0
        contrarest = 0
    elif x < 150:
        Roll = -15
        contrarest = 2
    else:
        Roll = -10
        contrarest = 2
    if y > 100:
        pitch = 15
        pcontrarest = -3
    elif y < 100:
        pitch = 5
        pcontrarest = -1
    else:
        pitch = 0
        pcontrarest = 0
    print 'Vertical adjustments', y, pitch,'##########################'
    print 'Horizontal adjustments', x, Roll,'##########################'
    if Roll != 0:
        # Move to the Centre
        drone.moveBebop(Roll, pitch, 0) 
        drone.wait(2)
        drone.moveBebop(contrarest, pcontrarest, 0) 
        drone.wait(1)
    
    # Hover
    drone.moveBebop(-1, 0, 0) 
    drone.moveBebop(1, 0, 0)
    drone.hover()
    
    # Take the pictures
    UAVPict("Left")
"""

####################################################################
"""
''' Function that creates a folder called "Photos" '''
def createFolder():
    # Create the name of the path
    file_path = "/home/bebopdev/kata/Photos/"
    directory = os.path.dirname(file_path)

    # If it does not exist, create it
    if not os.path.exists(directory):
        os.makedirs(directory)

''' Function that allows the drone to take 8 frames of a video '''
def UAVPict(Position):
    # Local variables
    i = 0

    try:
        # source fo the video
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
                
                # save images from the frame 11 to above
                if (i > 11):
                    # Save the image
                    imageName = "UAV_"+ Position + str(i - 11) +".jpg"
                    cv2.imwrite(imageName, img)
                    
                    # To erase later##########################################################
                    print 'Photo taken : ', Position
                    #########################################################################
                    
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
    drone.moveCamera(tilt= -80, pan=0)
    
    # go to the positio to take pictures    
    #drone.flyToAltitude(1.5)
    #drone.flyToAltitude(1.5)

    # Hover
    drone.moveBebop(-1, 0, 0) 
    drone.moveBebop(1, 0, 0)
    drone.moveBebop(0, 1, 0)
    
     # Take the pictures centre
    UAVPict("First")
    

    YawAngle = 30
    RollAngle = 9
    pitch = 9
    # Rotate
    drone.moveBebop(0, 1, 0)
    drone.wait(1)
    drone.moveBebop(0, 3, YawAngle)  
    drone.wait(2)
    drone.moveBebop(RollAngle,pitch,0)
    drone.wait(1)
    drone.moveBebop(0, 1, 0)
    # Take the pictures centre
    UAVPict("Second")

    YawAngle = 30
    RollAngle = 9
    pitch = 9
    # Rotate
    drone.moveBebop(0, 1, 0)
    drone.wait(1)
    drone.moveBebop(0, 5, YawAngle)  
    drone.wait(2)
    drone.moveBebop(RollAngle,pitch,0)
    drone.wait(1)
    
    # Take the pictures centre
    UAVPict("Third")

    
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
    #testCamera()

    # take off
    drone.takeoff()
    drone.flyToAltitude(1.5) 
    drone.moveBebop(0, 5, 0) 
    drone.flyToAltitude(1.5)      
    drone.moveBebop(0, 0, 0) 
    drone.wait(1)
    drone.hover()
    AerealFootage()    
    
    # return to the initial destination
    #drone.moveBebop(0, -5, 0) 
    #drone.wait(5)
    
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


"""
#########################################################################

"""
''' Function that makes the drone hover over the target and take pictures '''
def AerealFootage():
    
    # Adjust the camera 
    drone.moveCamera(tilt= -80, pan=0)
    
    # go to the positio to take pictures    
    drone.flyToAltitude(1.5)
    drone.flyToAltitude(1.5)

    # Center the target

    centred, x, y = takePict()
    if x > 150:
        Roll = 0
        contrarest = 0
    elif x < 150:
        Roll = -15
        contrarest = 2
    else:
        Roll = -10
        contrarest = 2
    print 'Horizontal adjustments', x, Roll,'##########################'
    if Roll != 0:
        # Move to the Centre
        drone.moveBebop(Roll, 1, 0) 
        drone.wait(2)
        drone.moveBebop(contrarest, -1, 0) 
        drone.wait(1)
    
    # Hover
    drone.moveBebop(-1, 0, 0) 
    drone.moveBebop(1, 0, 0)
    drone.moveBebop(0, 1, 0)
    
     # Take the pictures centre
    UAVPict("First")
    

    YawAngle = 24
    RollAngle = 8
    pitch = 6
    # Rotate
    drone.hover()
    drone.wait(1)
    drone.moveBebop(0, pitch, YawAngle)  
    drone.wait(2)
    drone.moveBebop(RollAngle,pitch,0)
    drone.wait(1)
    drone.hover()
    # Take the pictures centre
    UAVPict("Second")

    YawAngle = 24
    RollAngle = 8
    pitch = 11
    # Rotate
    drone.hover()
    drone.wait(1)
    drone.moveBebop(0, pitch, YawAngle)  
    drone.wait(2)
    drone.moveBebop(RollAngle,pitch,0)
    drone.wait(1)
    
    # Take the pictures centre
    UAVPict("Third")
"""
