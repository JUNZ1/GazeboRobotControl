#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Container classes and helpers methods
for Pioneer 3DX robot
"""

PKG = 'py3dx'
import roslib

roslib.load_manifest(PKG)

import rospy

from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import matplotlib.pyplot as plt

import time

class Robot(object):
    """
    Basic container class for Pioneer 3DX
    robot in ROS-Gazebo
    """

    def __init__(self, name):
        self.name = name

        # Publishers and subscribers
        self.odom = rospy.Subscriber("/%s/odom" % self.name, Odometry,
                                     self.odom_callback, queue_size=1)
        #self.front_laser = rospy.Subscriber("/%s/front_laser/scan" % self.name,LaserScan, self.laser_callback,queue_size=1)

        self.cmd_vel = rospy.Publisher("/%s/cmd_vel" % self.name, Twist,queue_size=10)

        #self.camera_data = rospy.Subscriber("/%s/front_camera/image_raw" % self.name, Image, self.image_subscriber)

        # Variables for subscriber data
        self.laser_data = None
        self.pose_data = None


    def odom_callback(self, msg):
        """
        Updates pose_data variable to
        data coming from odometry

        :param msg: Odometry callback data
        """
        self.pose_data = msg.pose.pose


    def laser_callback(self, msg):
        """
        Updates laser_data variable to
        data coming from front laser

        :param msg: LaserScan callback data
        """
        self.laser_data = msg.ranges
        plt.plot(self.laser_data)
        plt.draw()
        plt.cla()
        plt.clf()



    def stop_moving(self):
        """
        Sends an empty Twist message to velocity topic
        for stopping the robot
        """
        self.cmd_vel.publish(Twist())

    def dif_drive(self,linear,angular):
        move_cmd=Twist()
        move_cmd.linear.x=linear
        move_cmd.angular.z=angular
        self.cmd_vel.publish(move_cmd)

    def image_subscriber(self, image):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(image)
        except CvBridgeError, e:
            print e

        #print cv_image.shape
        cv2.imshow("Test", cv_image)
        #cv2.imwrite("Test.png", cv_image)
        cv2.waitKey(3)