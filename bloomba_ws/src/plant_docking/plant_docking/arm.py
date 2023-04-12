import rclpy
from std_msgs.msg import String
import serial

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=0.050)  # Replace '/dev/ttyACM0' with the name of your serial port

def callback(msg):
    
    message = msg.data
    print(f'Writing message: {message}')

    #Write to serial port
    if data!="":
        ser.write(message.encode('utf-8'))

    while ser.in_waiting:  # Or: while ser.inWaiting():
        line = ser.readline().decode('utf-8')
        print(f'I read: {line}')


def main(args=None):
    rclpy.init(args=args)
    node = rclpy.create_node('keyboard_publisher')
    subscription = node.create_subscription(String, 'keyboard', callback, 10)
    
    rate = node.create_rate(2)
    while rclpy.ok():
        rclpy.spin_once(node)
        rate.sleep()

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
