import paho.mqtt.client as mqtt

#서버로부터 CONNTACK 응답을 받을 때 호출되는 콜백
def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))
	#client.subscribe("$SYS/#")
	client.subscribe("home/#") #"/test"토픽 구독 7번줄

#서버로부터 publish message를 받을 때 호출되는 콜백
def on_message(client, userdata, msg):
	print(msg.topic+" "+str(msg.payload)) #토픽과 메세지를 출력한다.

client = mqtt.Client() #client 오브젝트 생성
client.on_connect = on_connect #콜백설정
client.on_message = on_message #콜백설정

client.connect("210.119.12.71") #Broker이라는 브로커에 연결, 브로커 주소 입력 17번줄
client.loop_forever()