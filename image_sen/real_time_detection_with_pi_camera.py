######## Webcam Object Detection Using Tensorflow-trained Classifier #########
#
# Author: Kim Dong Hun
# Date: 22/08/05
# Description:
# TensorFlow Lite를 활용하여 picamera로 센싱된 물체를 판단하는 프로그램
# 판단 가능 물체 :  teddy bear / bicycle / clock
# 그외의 물체를 인식하거나 판단을 1초안에 하지 못할 경우 예외처리

# Import packages
import os
import argparse
import cv2
import numpy as np
import sys
import time
import importlib.util
import paho.mqtt.client as mqtt
from threading import Thread
from tflite_runtime.interpreter import Interpreter

# Define VideoStream class to handle streaming of video from webcam in separate processing thread
class VideoStream:
    """Camera object that controls video streaming from the Picamera"""
    def __init__(self, resolution = (640, 480), framerate=30):
        # Initialize the PiCamera and the camera image stream
        self.stream = cv2.VideoCapture(0)
        ret = self.stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        ret = self.stream.set(3,resolution[0])
        ret = self.stream.set(4,resolution[1])

        # Read first frame from the stream
        (self.grabbed, self.frame) = self.stream.read()

    # Variable to control when the camera is stopped
        self.stopped = False

    def start(self):
    # Start the thread that reads frames from the video stream
        Thread(target=self.update,args=()).start()
        return self

    def update(self):
        # Keep looping indefinitely until the thread is stopped
        while True:
            # If the camera is stopped, stop the thread
            if self.stopped:
                # Close camera resources
                self.stream.release()
                return

            # Otherwise, grab the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
    # Return the most recent frame
        return self.frame

    def stop(self):
    # Indicate that the camera and thread should be stopped
        self.stopped = True

# 학습된 tflite 파일 경로 설정 준비
MODEL_NAME = "./Sample_model"
GRAPH_NAME = 'detect.tflite'
LABELMAP_NAME = 'labelmap.txt'
min_conf_threshold = flo/8t(0.7)
#VGA 640x480 4:3
imW, imH = int(640), int(480)

# 현재 작업 경로 불러오기
CWD_PATH = os.getcwd()

# detect.tflite 파일 불러오기
PATH_TO_CKPT = os.path.join(CWD_PATH, MODEL_NAME, GRAPH_NAME)

# labelmap.txt 파일 불러오기
PATH_TO_LABELS = os.path.join(CWD_PATH, MODEL_NAME, LABELMAP_NAME)

# labelmap.txt 리스트로 변환
with open(PATH_TO_LABELS, 'r') as f:
    labels = [line.strip() for line in f.readlines()]

# Have to do a weird fix for label map if using the COCO "starter model" from
# https://www.tensorflow.org/lite/models/object_detection/overview
# First label is '???', which has to be removed.
if labels[0] == '???':
    del(labels[0])

#tflite 확장자를 가진 모델을 메모리에 올림
interpreter = Interpreter(model_path = PATH_TO_CKPT)
interpreter.allocate_tensors()

# Get model details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
height = input_details[0]['shape'][1]
width = input_details[0]['shape'][2]



#서버로부터 CONNTACK 응답을 받을 때 호출되는 콜백
def on_connect(client, userdata, flags, rc):
    print("Ready")
    client.subscribe("/tes") #"/test"토픽 구독 7번줄

def on_disconnect(client, userdata, flags, msg = 0) :
    print("disconnect MQTT & Image_sensor Start")

#서버로부터 publish message를 받을 때 호출되는 콜백
#만약 받은 메시지가 'Image_sensor Start' 일 경우 전역변수인
#before_flag값을 True로 변경하여 client.loop 프로세스를 탈출
before_flag = False
def on_message(client, userdata, msg):
    recv_msg = msg.payload.decode('utf-8')

    if recv_msg == 'Image_sensor Start' :
        global before_flag
        before_flag = True


while True:
    client = mqtt.Client() #client 오브젝트 생성

    client.on_connect = on_connect #콜백설정
    client.on_disconnect = on_disconnect #콜백설정
    client.on_message = on_message #콜백설정

    client.connect("210.119.12.71") #Broker이라는 브로커에 연결

    #이미지 분석 시작 전 프로세스
    #loop 함수를 통해 0.1초마다 MQTT 브로커로부터 들어온 데이터가 존재하는지 확인
    while True :
        client.loop(0.1)

        if before_flag is True:
            before_flag = False
            client.disconnect()
            break

    object_name = ""
    run_time_flag = False

    videostream = VideoStream(resolution=(imW, imH), framerate = 30).start()
    time.sleep(1)

    #이미지 분석 프로세스
    start_time = time.time()
    while True:
        now_time = time.time()
        uptime = now_time - start_time

        if uptime > 30 : 
            run_time_flag = True
            object_name = "Error"
            break

        frame1 = videostream.read()

        # Acquire frame and resize to expected shape [1xHxWx3]
        frame = frame1.copy()
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb, (width, height))
        input_data = np.expand_dims(frame_resized, axis=0)

        # Perform the actual detection by running the model with the image as input
        interpreter.set_tensor(input_details[0]['index'], input_data)
        interpreter.invoke()

        # Retrieve detection results
        boxes = interpreter.get_tensor(output_details[0]['index'])[0] # Bounding box coordinates of detected objects
        classes = interpreter.get_tensor(output_details[1]['index'])[0] # Class index of detected objects
        scores_bef = interpreter.get_tensor(output_details[2]['index'])[0] # Confidence of detected objects

        # 가장 score가 높은 object 선별
        scores_asc = np.sort(scores_bef)
        scores = scores_asc[::-1]

        if (min_conf_threshold < scores[0] <= 1.0):

            # Look up object name from "labels" array using class index
            object_name = labels[int(classes[0])] 
            print(object_name)

            if object_name == "teddy bear" or object_name == "bicycle" or object_name == "clock":
                break
        
        #cv2.imshow('Object detector', frame)
        
        # Press 'q' to quit
        if cv2.waitKey(1) == ord('q'):
            break


    #이미지 분석 시작 후 프로세스
    mqttc = mqtt.Client("python_pub")      # MQTT Client 오브젝트 생성
    mqttc.connect("210.119.12.71", 1883)    # MQTT 서버에 연결
    mqttc.publish("/Image_res", object_name)  # '/test' 토픽에 "Hello World!"라는 메시지 발행
    print(object_name)
    mqttc.disconnect()

    # Clean up
    #cv2.destroyAllWindows()
    videostream.stop()
