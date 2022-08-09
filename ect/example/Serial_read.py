import serial

while True :
	recv_Serial = serial.Serial('/dev/ttyUSB0', 9600)
	print(recv_Serial.readline())