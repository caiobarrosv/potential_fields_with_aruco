#!/usr/bin/env python
# Code available in
# https://github.com/neobotix/neo_simulation
import rospy
import tf
import rospkg
from gazebo_msgs.srv import SpawnModel, GetModelState
import time
from geometry_msgs.msg import *
from gazebo_msgs.msg import ModelState, ModelStates
import os
from os.path import expanduser
from pathlib import Path
from tf import TransformListener
from tf.transformations import quaternion_from_euler

rospack = rospkg.RosPack()
Home = rospack.get_path('custom_codes')
path = Home + '/models/box/model.sdf'


class Moving():
    def __init__(self, model_name, Spawning1, y_pose, x_pose, z_pose, oriFinal):
        self.pub_model = rospy.Publisher('gazebo/set_model_state', ModelState, queue_size=1)
        self.model_name = model_name
        self.rate = rospy.Rate(10)
        self.x_model_pose = x_pose
        self.y_model_pose = y_pose
        self.z_model_pose = z_pose
        self.Spawning1 = Spawning1
        self.orientation = oriFinal

    def spawning(self,):
		with open(path) as f:
			product_xml = f.read()
		item_name = "product_{0}_0".format(0)
		print("Spawning model:%s", self.model_name)
		# X and Y positions are somewhat in an incorrect order in Gazebo
		item_pose = Pose(Point(x=self.y_model_pose, y=self.x_model_pose,z=self.z_model_pose),
						 Quaternion(self.orientation[0], self.orientation[1], self.orientation[2], self.orientation[3]))
		self.Spawning1(self.model_name, product_xml, "", item_pose, "world")

    def moving_goal(self):
        obstacle = ModelState()
        ptFinal, oriFinal = tf.lookupTransform("base_link", "ar_marker_0", rospy.Time(0))
        obstacle.model_name = self.model_name
        obstacle.pose = model.pose[i]
        obstacle.twist = Twist()
        obstacle.twist.linear.y = 1.3
        obstacle.twist.angular.z = 0
        self.pub_model.publish(obstacle)

def main():
    rospy.init_node('Spawning_APF_Goal')
    Spawning1 = rospy.ServiceProxy("gazebo/spawn_sdf_model", SpawnModel)
    rospy.wait_for_service("gazebo/spawn_sdf_model")
    model_coordinates = rospy.ServiceProxy(
        '/gazebo/get_model_state', GetModelState)
    object_coordinates = model_coordinates("robot", "")
    z_position = object_coordinates.pose.position.z
    y_position = object_coordinates.pose.position.y
    x_position = object_coordinates.pose.position.x

    print "X, Y, Z: ", x_position, y_position, z_position

    # This is the position of the object spawned in gazebo relative to the base_link
    ptFinal = [-0.5, 0.1, 0.05]
    oriFinal = quaternion_from_euler(0.0, 0.0, -0.6)
    
    moving1 = Moving("custom_box", Spawning1, x_position - ptFinal[1], y_position + ptFinal[0], z_position + ptFinal[2], oriFinal)
    moving1.spawning()

    # while not rospy.is_shutdown():
    	# moving.moving_goal()

if __name__ == '__main__':
    main()
