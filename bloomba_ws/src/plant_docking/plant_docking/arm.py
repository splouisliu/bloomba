import rclpy
from std_msgs.msg import String
import serial

ser = serial.Serial('/dev/ttyACM0', 9600)  # Replace '/dev/ttyACM0' with the name of your serial port
ser.timeout = 1

def callback(msg):
    
    message = msg.data
    print(f'Writing message: {message}')

    #Write to serial port
    ser.write(message.encode('utf-8'))

    line = ser.readline().decode('utf-8')
    print(f'I read: {line}')


def main(args=None):
    rclpy.init(args=args)
    node = rclpy.create_node('keyboard_publisher')
    subscription = node.create_subscription(String, 'keyboard', callback, 10)

    while rclpy.ok():
        rclpy.spin_once(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
