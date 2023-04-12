"""
Procedure to remote watering arm:

source install/local_setup.bash
ros2 run plant_docking watering_arm 
ros2 topic pub /keyboard std_msgs/String "data: 'l0.1'" --once

*This will lower watering arm by 10 cm, activate pump, then raise watering arm back up
*Keep in mind launching watering_arm node will cause pump to activate. Be ready to catch water.


"""


import rclpy
from std_msgs.msg import String
import serial

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=0.050)  # Replace '/dev/ttyACM0' with the name of your serial port

def callback(msg):
    
    message = msg.data
    print(f'Writing message: {message}')

    #Write to serial port
    if msg.data!="":
        ser.write(message.encode('utf-8'))

    #while ser.in_waiting:  # Or: while ser.inWaiting():
    line = ser.readline().decode('utf-8')
    print(f'I read: {line}')


def main(args=None):
    rclpy.init(args=args)
    node = rclpy.create_node('keyboard_publisher')
    subscription = node.create_subscription(String, 'keyboard', callback, 10)
    
    #rate = node.create_rate(1000)
    while rclpy.ok():
        rclpy.spin_once(node)
        #rate.sleep()

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
