#!/usr/bin/python
"""
  ARDrone3 demo with autonomous navigation to two color Parrot Cap
  usage:
       ./demo.py <task> [<metalog> [<F>]]
"""
import sys
import cv2
import os
import time
import signal

from bebop import Bebop
from commands import movePCMDCmd
from capdet import detectTwoColors, loadColors
from bebop import *
# this will be in new separate repository as common library fo robotika Python-powered robots
from apyros.metalog import MetaLog, disableAsserts
from apyros.manual import myKbhit, ManualControlException

import time


drone = Bebop()
print "Battery:", drone.battery
sys.exit(0)
