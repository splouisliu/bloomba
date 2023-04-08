import math

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient

from geometry_msgs.msg import Twist

#need to import tf messages, not just String type messages.
#/tf actually publishes messages of type tf2_msgs
from geometry_msgs.msg import PoseStamped
from tf2_msgs.msg import TFMessage

from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener
from irobot_create_msgs.action import RotateAngle

# Stop the robot when it no longer sees an april tag (clear the buffer)
# Tune travel velocities (robot is overshooting)

class RotateActionClient(Node):

    def __init__(self):
        super().__init__('rotate_action_client')
        self._action_client = ActionClient(self, RotateAngle, 'rotate_angle')

    def send_goal(self):
        goal_msg = RotateAngle.Goal()
        goal_msg.angle = 6.28/15 #Spin in 15 degree increments
        goal_msg.max_rotation_speed = 1.0

        self._action_client.wait_for_server()
        print(1)

        return self._action_client.send_goal_async(goal_msg)
    

class FrameListener(Node):

    def __init__(self):
        super().__init__('frame_listener')
        self.target_frame = self.declare_parameter(
          'target_frame', 'turtle1').get_parameter_value().string_value
        
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 1) #TODO: USE THIS to publish velocities to the Create 3
        #Calls on_timer() every 1 second
        self.timer = self.create_timer(0.5, self.tf_on_timer)

    def tf_on_timer(self):
        from_frame_rel = self.target_frame
        to_frame_rel = 'plant_pot1'
        msg = Twist()
        has_reached_goal = False
        has_found_tag = False
        spin_start = False
        time_at_spin_start = 0

        
        try:
            t = self.tf_buffer.lookup_transform( #search the buffer for transforms 
            to_frame_rel, #destination  frame
            from_frame_rel, #source  frame
            rclpy.time.Time()) #Time at which we want to transform (for now, it's just the latest available transform)
            has_found_tag = True

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

            if t.transform.translation.z > 0.35:
                msg.linear.x = 0.3

            elif t.transform.translation.z < 0.30:
                msg.linear.x = -0.3

            #Publish velocities
            self.publisher.publish(msg)

            # Clear the buffer, but don't set has_found_tag to false.
            #self.tf_buffer = Buffer()
            
        except TransformException as ex:
            self.get_logger().info(
            f'Could not transform {to_frame_rel} to {from_frame_rel}: {ex}')

            #Spin the robot if we have not found the tag
            # if ~has_found_tag & (rclpy.time.Time().nanoseconds-time_at_spin_start < 10000000000):
            #     msg.angular.z = 0.4

            #     if ~spin_start:
            #         time_at_spin_start = rclpy.time.Time().nanoseconds
            #         spin_start = True

            # else:
            #     #Stop the robot if we lost track of the tag
            #     msg.angular.z = 0.0
            #     msg.linear.x = 0.0

            # self.publisher.publish(msg)
            return
        

        #Want angular speed to be constant until robot faces the tag
        ## convert from quaternion to phi
        #Want forward speed to be constant until robot is at a point 30 cm directly in front of the center of the tag 
        #Remember that min sense distance of camera is 20 cm
        ## z variable is forward distance, x variable is lateral distance.
        ## find a point 30 cm directly in front of the center of the April Tag.
        #Later, tell the watering arm to lower/raise up to plant pot height.

        # yaw_ref = 180
        # msg.angular.z = scale_rotation_rate * math.atan2(
        #     t.transform.translation.z,
        #     t.transform.translation.x)
        
        #(yaw_deg-yaw_ref)

        # scale_forward_speed = 0.5
        # msg.linear.x = scale_forward_speed * math.sqrt(
        #     t.transform.translation.x ** 2 +
        #     t.transform.translation.z ** 2)
        


def main(args=None):
    rclpy.init(args=args)

    frame_listener = FrameListener()
    action_client = RotateActionClient()
    rate = frame_listener.create_rate(2)


    future = action_client.send_goal()
    try:
        for i in range(24):
            #Spin one first, then when april tag detected spin the next node.
            rclpy.spin_until_future_complete(action_client,future)
            rclpy.spin_once(frame_listener)
            rate.sleep()

    except KeyboardInterrupt:
        pass
    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    #frame_listener.destroy_node()
    rclpy.shutdown()
    
# def main(args=None):
#         rclpy.init(args=args)

#         action_client = RotateActionClient()

#         print(2)

#         future = action_client.send_goal()

#         rclpy.spin_until_future_complete(action_client,future)

if __name__ == '__main__':
    main()