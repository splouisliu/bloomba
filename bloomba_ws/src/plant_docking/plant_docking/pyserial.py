import serial

# Configure serial port
ser = serial.Serial('/dev/ttyACM0', 9600)  # Replace 'COM1' with the name of your serial port
ser.timeout = 1  # Set a timeout for reading from the serial port

# Loop to read keyboard input and send serial messages
while True:
    message = input("Enter message to send: ")
    ser.write(message.encode('utf-8'))
    line = ser.readline().decode('utf-8')
    print(f'I read: {line}')
