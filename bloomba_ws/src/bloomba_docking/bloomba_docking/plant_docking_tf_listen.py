import math

import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from geometry_msgs.msg import Twist

#need to import tf messages, not just String type messages.
#/tf actually publishes messages of type tf2_msgs
from geometry_msgs.msg import PoseStamped
from tf2_msgs.msg import TFMessage

from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener

class FrameListener(Node):

    def __init__(self):
        super().__init__('frame_listener')
        self.target_frame = self.declare_parameter(
          'target_frame', 'turtle1').get_parameter_value().string_value
        
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.publisher = self.create_publisher(Twist, 'turtle2/cmd_vel', 1)

        #Calls on_timer() every 1 second
        self.timer = self.create_timer(0.5, self.tf_on_timer)


    def tf_on_timer(self):
        from_frame_rel = self.target_frame
        to_frame_rel = 'plant_pot1'
        
        try:
            t = self.tf_buffer.lookup_transform( #search the buffer for transforms 
            to_frame_rel, #destination  frame
            from_frame_rel, #source  frame
            rclpy.time.Time()) #Time at which we want to transform (for now, it's just the latest available transform)
            self.get_logger().info(
            f'\n X pos: {t.transform.translation.x} \n Y pos: {t.transform.translation.y} \n Z pos: {t.transform.translation.z}\n') 

        except TransformException as ex:
            self.get_logger().info(
            f'Could not transform {to_frame_rel} to {from_frame_rel}: {ex}')
            return
        


def main():
    rclpy.init()

    frame_listener = FrameListener()

    try:
        rclpy.spin(frame_listener)
    except KeyboardInterrupt:
        pass
    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    #frame_listener.destroy_node()
    rclpy.shutdown()


# if __name__ == '__main__':
#     main()