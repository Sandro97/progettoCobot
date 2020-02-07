#!/usr/bin/env python

#Importa librerie necessarie
import argparse
import numpy as np
import cv2
from cv_bridge import CvBridge, CvBridgeError
import rospy
import intera_interface

#FUnzione che avvia lo streaming con la fotocamera
def accendiCamera():
    rp = intera_interface.RobotParams()
    valid_cameras = rp.get_camera_names()
    if not valid_cameras:
        rp.log_message(("Cannot detect any camera_config"
            " parameters on this robot. Exiting."), "ERROR")
        return
    camera="right_hand_camera"
    gain=-1
    exposure=-1
    use_canny_edge = False

    print("Initializing node... ")
    rospy.init_node('camera_display', anonymous=True)

    cameras = intera_interface.Cameras()

    if not cameras.verify_camera_exists(camera):
        rospy.logerr("Could not detect the specified camera, exiting the example.")
        return
    rospy.loginfo("Opening camera '{0}'...".format(camera))

    cameras.start_streaming(camera)

    # optionally set gain and exposure parameters
    if gain is not -1:
        if cameras.set_gain(camera, gain):
            rospy.loginfo("Gain set to: {0}".format(cameras.get_gain(camera)))

    if exposure is not -1:
        if cameras.set_exposure(camera, exposure):
            rospy.loginfo("Exposure set to: {0}".format(cameras.get_exposure(camera)))

    return cameras
