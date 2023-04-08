import rclpy
# import rospy
from rclpy.action import ActionClient
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
import time
import math

from irobot_create_msgs.action import RotateAngle

from geometry_msgs.msg import Twist
from tf2_msgs.msg import TFMessage

from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener
from irobot_create_msgs.action import RotateAngle

future = rclpy.Future()
has_found_tag = False

class FrameListener(Node):

    def __init__(self):
        super().__init__('frame_listener')
        self.target_frame = 'camera'
        
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 1) #TODO: USE THIS to publish velocities to the Create 3
        #Calls on_timer() every 1 second
        self.timer = self.create_timer(0.5, self.tf_on_timer)

    def tf_on_timer(self):
        from_frame_rel = self.target_frame
        to_frame_rel = 'plant_pot1'
        print("Inside Timer")
        msg = Twist()
        has_reached_goal = False
        spin_start = False
        time_at_spin_start = 0
        
        try:
            t = self.tf_buffer.lookup_transform( #search the buffer for transforms 
            to_frame_rel, #destination  frame
            from_frame_rel, #source  frame
            rclpy.time.Time()) #Time at which we want to transform (for now, it's just the latest available transform)
            has_found_tag = True
            print("try")

            #Stop spinning the robot
            msg.angular.z = 0.0
            
            self.get_logger().info(
            f'\n X pos: {t.transform.translation.x} \n Y pos: {t.transform.translation.y} \n Z pos: {t.transform.translation.z}\n') 
            
            correctedX = t.transform.translation.x*4/3 #Correct these values because the sensor is always off by 25% lower
            correctedY = t.transform.translation.y*4/3
            correctedZ = t.transform.translation.z*4/3

            self.get_logger().info(
            f'\n Corrected X pos: {correctedX} \n Corrected Y pos: {correctedY} \n Corrected Z pos: {correctedZ}\n') 

            #TODO: Find the yaw (phi) from a quaternion
            q_x = t.transform.rotation.x
            q_y = t.transform.rotation.y
            q_z = t.transform.rotation.z
            q_w = t.transform.rotation.w

            yaw = math.atan2(2.0*(q_y*q_z+q_w*q_x),q_w*q_w-q_x*q_x-q_y*q_y+q_z*q_z)
            yaw_deg = yaw*180/math.pi

            self.get_logger().info(
            f'\n Yaw: {yaw_deg} \n') 

            # if t.transform.translation.z > 0.35:
            #     msg.linear.x = 0.3

            # elif t.transform.translation.z < 0.30:
            #     msg.linear.x = -0.3

            # #Publish velocities
            # self.publisher.publish(msg)

            # Clear the buffer, but don't set has_found_tag to false.
            #self.tf_buffer = Buffer()

            print(123)
            
        except TransformException as ex:
            self.get_logger().info(
            f'Could not transform {to_frame_rel} to {from_frame_rel}: {ex}')
            return
        

class RotateActionClient(Node):

    def __init__(self):
        super().__init__('rotate_action_client')
        self._action_client = ActionClient(self, RotateAngle, 'rotate_angle')

    def send_goal(self, angle_goal):
        goal_msg = RotateAngle.Goal()
        goal_msg.angle = angle_goal
        goal_msg.max_rotation_speed = 1.0

        self._action_client.wait_for_server()
        print(1)

        return self._action_client.send_goal_async(goal_msg)


def main(args=None):
    rclpy.init(args=args)
    executor = MultiThreadedExecutor()

    action_client = RotateActionClient()
    frame_listener = FrameListener()

    counter = 0
    while rclpy.ok & (counter < 24):
        rclpy.spin_once(frame_listener,timeout_sec=0.5)
        
        if has_found_tag:
            break

        #Turn 15 degrees
        angle_goal = 6.28/15
        action_client.send_goal(angle_goal=angle_goal)
        counter +=1

    print("found the tag")
    rclpy.spin(frame_listener)


if __name__ == '__main__':
    
    main()