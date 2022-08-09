import serial
import time
while True:
	com = serial.Serial(port = "/dev/ttyUSB0",
			baudrate = 9600,
			bytesize = serial.EIGHTBITS,
			parity = serial.PARITY_NONE,
			timeout = 1)
	s = "1"
	com.write(s.encode())
	time.sleep(1)