import serial
import paho.mqtt.client as mqtt

trans_Serial = serial.Serial(port = "/dev/ttyUSB0",
			baudrate = 9600,
			bytesize = serial.EIGHTBITS,
			parity = serial.PARITY_NONE,
			timeout = 1)						#송신
recv_Serial = serial.Serial('/dev/ttyUSB0', 9600)		#수신
mqttc = mqtt.Client("python_pub")				#mqtt 송신
mqttc.connect("210.119.12.71", 1883)

def on_connect2(client, userdata, flags, rc) :
	print("start mqtt2")
	client.subscribe("/test2")

def on_connect5(client, userdata, flags, rc) :
	print("start mqtt5")
	client.subscribe("/test5")

def on_message(client, userdata, msg):
	MQTT_value = msg.payload
	MQTT_value = MQTT_value.decode('utf-8')
	print("MQTT : " + MQTT_value)
	client.disconnect()
	trans_Serial.write(MQTT_value.encode())

def MQTT(a) :
	client = mqtt.Client()
	if a==2 :
		client.on_connect = on_connect2

	elif a==5 :
		client.on_connect = on_connect5

	client.on_message = on_message
	client.connect("210.119.12.71")
	client.loop_forever()			#mqtt 수신시까지 무한 대기

while True :
	value=recv_Serial.readline()	#첫번째 적외선 제어 수신
	value=value.strip()				#\r\n 제거
	value=value.decode('utf-8')		# b제거
	print("적외선1 : " +value)
	mqttc.publish("/test1", value)	#루틴1 완료

	MQTT(2)							#루틴2 완료

	value=recv_Serial.readline()	#두번째 적외선 제어 수신
	value=value.strip()
	value=value.decode('utf-8')
	print("적외선2 : " + value)
	mqttc.publish("/test3", value)	#루틴3 완료

	value = recv_Serial.readline()	#박스 적외선 제어 수신
	value = value.strip()
	value = value.decode('utf-8')
	print("박스 : " + value)
	mqttc.publish("/test4", value)

	#MQTT(5)	#마지막에 필요할듯 함

	# 아두이노 Read버퍼 초기화용#
	str = 'reset'
	trans_Serial.write(str.encode())

