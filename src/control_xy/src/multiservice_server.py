#!/usr/bin/env python3

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal, MoveBaseActionGoal
from std_srvs.srv import Empty, EmptyResponse  # Import Empty and EmptyResponse
from geometry_msgs.msg import Twist
from actionlib_msgs.msg import GoalID

stop_command = Twist()
move_base_client = None

def stop_movement_callback(req):
    global move_base_client

    if move_base_client is None:
        rospy.loginfo("No active goal to stop.")
        return EmptyResponse()

    # Create a GoalID message with an empty ID to cancel the current goal
    goal_cancel_msg = GoalID()
    goal_cancel_msg.id = ""

    # Publish the GoalID message to the move_base/cancel topic
    cancel_publisher.publish(goal_cancel_msg)

    rospy.loginfo("Stop!.")
    return EmptyResponse()

def send_goal(x, y):
    global move_base_client

    move_base_client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    move_base_client.wait_for_server()

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = 'map'
    goal.target_pose.pose.position.x = x
    goal.target_pose.pose.position.y = y
    goal.target_pose.pose.orientation.w = 1.0

    move_base_client.send_goal(goal)
    move_base_client.wait_for_result()

    if move_base_client.get_state() == actionlib.GoalStatus.SUCCEEDED:
        rospy.loginfo("Goal reached successfully!")
    else:
        rospy.loginfo("Failed to reach the goal.")

def go_home_callback(req):
    rospy.loginfo("Going to home.")
    send_goal(2, 1)

def go_to_kitchen_callback(req):
    rospy.loginfo("Going to kitchen.")
    send_goal(-1, -2)

if __name__ == '__main__':
    rospy.init_node('multiservice_server')

    # Create a publisher for the move_base/cancel topic
    cancel_publisher = rospy.Publisher('move_base/cancel', GoalID, queue_size=10)

    service1 = rospy.Service('go_home', Empty, go_home_callback)
    service2 = rospy.Service('go_to_kitchen', Empty, go_to_kitchen_callback)
    service3 = rospy.Service('stop', Empty, stop_movement_callback)

    rospy.loginfo("Multiservice server is running.")
    rospy.spin()
