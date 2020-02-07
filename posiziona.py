#!/usr/bin/env python

# Import the necessary Python modules

import rospy                         # rospy - ROS Python API
import intera_interface              # intera_interface - Sawyer Python API
from numpy import deg2rad

def posiziona():
    Z_POSITION = {'right_j6': deg2rad(181.85), 'right_j5': deg2rad(4.56), 'right_j4': deg2rad(-27.1), 'right_j3': deg2rad(50.51), 'right_j2': deg2rad(-22.28), 'right_j1': deg2rad(-51.92), 'right_j0': deg2rad(20.11)}
    Z_HEAD=deg2rad(-24.0)

    rospy.init_node('Hello_Sawyer')     # initialize our ROS node, registering it with the Master

    limb = intera_interface.Limb('right')   # create an instance of intera_interface's Limb class
    head = intera_interface.Head()          # create an instance of Head class

    #Move to zero position
    limb.move_to_joint_positions(Z_POSITION)
    head.set_pan(Z_HEAD)



    # quit
    #quit()
