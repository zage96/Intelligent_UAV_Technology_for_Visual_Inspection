# Intelligent UAV Technology for Visual Inspection

In this repository, it is shown the design and development process of an autonomous 
UAV system used for visual inspection. The results and evaluations obtained for the 
system are presented as well. The code make the drone capable of flying to an specific 
location, indicated by a marker through the use of color recognition, and take pictures of 
the location. Afterwards, the images are merged together giving the user a bigger view of 
the area around and of the marker. 

Different python libraries were used in order to control the drone movements, and the image processing.


Using a  [Parrot Bebop drone](https://wiki.paparazziuav.org/wiki/Bebop) and the  [Katarina](https://github.com/robotika/katarina) python library a program was created for the drone to operate autonomously and find a specific target.

![bebop](./Bebop_drone.PNG?raw=true)

For this project, some blue tubes were used as the target to be located:
![target](./Target_recognition.PNG?raw=true)

Once the target was located, the drone would fly to it, ans start taking areal photos which were then [merged](https://github.com/zage96/Intelligent_UAV_Technology_for_Visual_Inspection/blob/main/MergingImages/MergeImages.py) into one and delivered to the user.

![left](./MergingImages/UAV_Left2.jpg?raw=true)
![center](./MergingImages/UAV_Centre4.jpg?raw=true)
![right](./MergingImages/UAV_Right7.jpg?raw=true)

Merged image:
![merged](./MergingImages/MergeImages.jpg?raw=true)
