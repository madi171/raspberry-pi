# coding:utf-8
'''
'''
import os
from socket import *
from time import ctime
import binascii
import RPi.GPIO as GPIO
import time
import threading
from smbus import SMBus
import cv2
import numpy as np
from keras.models import Sequential
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.layers.core import Activation
from keras.layers.core import Flatten
from keras.layers.core import Dense
from keras import backend as K

IMAGE_SIZE = 64

"""
    PiCameraClassication
    A demo for pi-car following object detected by DNN model
    
"""
class PiCameraClassication:
    def __init__():
        self.data = []
        self.labels = []
        self.model = self.build_model()
        pass

    def gen_training_image_set(self):
        # loop over the input images
        for imagePath in imagePaths:
            # load the image, pre-process it, and store it in the data list
            image = cv2.imread(imagePath)
            image = cv2.resize(image, (IMAGE_SIZE, IMAGE_SIZE))
            image = img_to_array(image)
            self.data.append(image)

            # extract the class label from the image path and update the
            # labels list
            label = imagePath.split(os.path.sep)[-2]
            label = 1 if label == "apple" else 0
            self.labels.append(label)

        # scale the raw pixel intensities to the range [0, 1]
        self.data = np.array(self.data, dtype="float") / 255.0
        self.labels = np.array(self.labels)

    def build_model(self):
        self.model = LeNet.build(width=28, height=28, depth=3, classes=2)
        opt = Adam(lr=INIT_LR, decay=INIT_LR / EPOCHS)
        self.model.compile(loss="binary_crossentropy", optimizer=opt, metrics=["accuracy"])
        pass

    def train(self):
        # split train and test set
        (trainX, testX, trainY, testY) = train_test_split(self.data, self.labels, test_size=0.25, random_state=42)

        # convert the labels from integers to vectors
        trainY = to_categorical(trainY, num_classes=2)
        testY = to_categorical(testY, num_classes=2)

        self.model.fit(trainX, trainY, batch_size=32, epochs=10, verbose=1)

        pass

    def predict(self, img_frame):
        img_frame = cv2.resize(img_frame, (IMAGE_SIZE, IMAGE_SIZE))
        img_frame = img_to_array(img_frame)
        data = np.array([img_frame])

        ret = self.model.predict(data)

        if len(ret) > 0:
            return ret[0]
        pass

    def save_model(self):
        self.model.save("mnistmodel.h5")
        pass

    def load_model(self):
        self.model = load_model("mnistmodel.h5")
        pass

    def following(self):


def Path_Dect_img_processing(func):
    global Path_Dect_px
    global Path_Dect_on
    Path_Dect_fre_count = 0
    Path_Dect_px_sum = 0
    Path_Dect_cap = 0
    print("into theads Path_Dect_img_processing")
    while True:
        if (Path_Dect_on):
            if (Path_Dect_cap == 0):
                cap = cv2.VideoCapture(0)
                Path_Dect_cap = 1
            else:
                Path_Dect_fre_count += 1
                ret, img_frame = cap.read()  # capture frame_by_frame
                img_frame_gray = cv2.cvtColor(img_frame, cv2.COLOR_BGR2GRAY)  # get gray img
                ret, img_frame_gray_bin = cv2.threshold(img_frame_gray, 70, 255, cv2.THRESH_BINARY)  # binaryzation 二值化
                for j in range(0, 640, 5):
                    if img_frame_gray_bin[240, j] == 0:
                        Path_Dect_px_sum = Path_Dect_px_sum + j
                Path_Dect_px = Path_Dect_px_sum >> 5
                Path_Dect_px_sum = 0
                Path_Dect_fre_count = 0
        elif (Path_Dect_cap):
            Motor_Stop()
            time.sleep(0.001)
            Path_Dect_cap = 0
            cap.relese()


####################################################
##函数名称 Communication_Decode()
##函数功能 ：通信协议解码
##入口参数 ：无
##出口参数 ：无
####################################################    
def Communication_Decode():
    global RevStatus
    global TurnAngle
    global Golength
    global Pre_Cruising_Flag
    global Cruising_Flag
    global motor_flag
    global left_speed
    global right_speed
    global left_speed_hold
    global right_speed_hold
    global Path_Dect_on
    print 'Communication_decoding...'
    if buffer[0] == '00':
        if buffer[1] == '01':  # 前进
            Motor_Forward()
        elif buffer[1] == '02':  # 后退
            Motor_Backward()
        elif buffer[1] == '03':  # 左转
            Motor_TurnLeft()
        elif buffer[1] == '04':  # 右转
            Motor_TurnRight()
        elif buffer[1] == '00':  # 停止
            Motor_Stop()
        else:
            Motor_Stop()
    elif buffer[0] == '02':
        if buffer[1] == '01':  # 左速度
            speed = hex(eval('0x' + buffer[2]))
            speed = int(speed, 16)
            ENA_Speed(speed)
        elif buffer[1] == '02':  # 右侧速度
            speed = hex(eval('0x' + buffer[2]))
            speed = int(speed, 16)
            ENB_Speed(speed)
    elif buffer[0] == '01':
        if buffer[1] == '01':  # 1号舵机驱动
            SetServoAngle(1, buffer[2])
        elif buffer[1] == '02':  # 2号舵机驱动
            SetServoAngle(2, buffer[2])
        elif buffer[1] == '03':  # 3号舵机驱动
            SetServoAngle(3, buffer[2])
        elif buffer[1] == '04':  # 4号舵机驱动
            SetServoAngle(4, buffer[2])
        elif buffer[1] == '05':  # 5号舵机驱动
            SetServoAngle(5, buffer[2])
        elif buffer[1] == '06':  # 6号舵机驱动
            SetServoAngle(6, buffer[2])
        elif buffer[1] == '07':  # 7号舵机驱动
            SetServoAngle(7, buffer[2])
        elif buffer[1] == '08':  # 8号舵机驱动
            SetServoAngle(8, buffer[2])
        else:
            print '舵机角度大于170'
    elif buffer[0] == '13':
        if buffer[1] == '01':
            Cruising_Flag = 1  # 进入红外跟随模式
            print 'Cruising_Flag红外跟随模式 %d ' % Cruising_Flag
        elif buffer[1] == '02':  # 进入红外巡线模式
            Cruising_Flag = 2
            print 'Cruising_Flag红外巡线模式 %d ' % Cruising_Flag
        elif buffer[1] == '03':  # 进入红外避障模式
            Cruising_Flag = 3
            print 'Cruising_Flag红外避障模式 %d ' % Cruising_Flag
        elif buffer[1] == '04':  # 进入超声波壁障模式
            Cruising_Flag = 4
            print 'Cruising_Flag超声波壁障 %d ' % Cruising_Flag
        elif buffer[1] == '05':  # 进入超声波距离PC显示
            Cruising_Flag = 5
            print 'Cruising_Flag超声波距离PC显示 %d ' % Cruising_Flag
        elif buffer[1] == '06':
            Cruising_Flag = 6
            print 'Cruising_Flag超声波遥控壁障 %d ' % Cruising_Flag
        elif buffer[1] == '07':
            left_speed_hold = left_speed
            right_speed_hold = right_speed
            tcpCliSock.send("\xFF")
            time.sleep(0.005)
            tcpCliSock.send("\xA8")
            time.sleep(0.005)
            tcpCliSock.send("\x00")
            time.sleep(0.005)
            tcpCliSock.send("\x00")
            time.sleep(0.005)
            tcpCliSock.send("\xFF")
            time.sleep(0.005)
            Cruising_Flag = 7
        elif buffer[1] == '08':
            if buffer[2] == '00':  # Path_Dect 调试模式
                Path_Dect_on = 0
                Cruising_Flag = 8
                print 'Cruising_Flag Path_Dect调试模式 %d ' % Cruising_Flag
            # os.system('sh start_mjpg_streamer.sh')
            elif buffer[2] == '01':  # Path_Dect 循迹模式
                os.system('sh stop_mjpg_streamer.sh')
                time.sleep(2)
                Path_Dect_on = 1
                Cruising_Flag = 9
                print 'Cruising_Flag Path_Dect循迹模式 %d ' % Cruising_Flag
        elif buffer[1] == '00':
            RevStatus = 0
            Cruising_Flag = 0
            print 'Cruising_Flag正常模式 %d ' % Cruising_Flag
    # else:
    # Cruising_Flag = 0
    elif buffer[0] == 'a0':
        RevStatus = 2
        Tangle = hex(eval('0x' + buffer[1]))
        Tangle = int(Tangle, 16)
        TurnAngle = Tangle
        Golen = hex(eval('0x' + buffer[2]))
        Golen = int(Golen, 16)
        Golength = Golen
    elif buffer[0] == 'a1':
        RevStatus = 1
        Tangle = hex(eval('0x' + buffer[1]))
        Tangle = int(Tangle, 16)
        TurnAngle = Tangle
        Golen = hex(eval('0x' + buffer[2]))
        Golen = int(Golen, 16)
        Golength = Golen
    elif buffer[0] == '40':
        temp = hex(eval('0x' + buffer[1]))
        temp = int(temp, 16)
        print 'mode_flag====== %d ' % temp
        motor_flag = temp
    elif buffer[0] == '32':  # 存储角度
        XRservo.XiaoRGEEK_SaveServo()
    elif buffer[0] == '33':  # 读取角度
        XRservo.XiaoRGEEK_ReSetServo()
    elif buffer[0] == '04':  # 开关灯模式 FF040000FF开灯  FF040100FF关灯
        if buffer[1] == '00':
            Open_Light()
        elif buffer[1] == '01':
            Close_Light()
        else:
            print 'error1 command!'
    elif buffer[0] == '05':  # 读取电压 FF050000FF
        if buffer[1] == '00':
            Vol = XRservo.XiaoRGEEK_ReadVol()
            print 'Read_Voltage %d ' % Vol
        else:
            print 'error2 command!'
    elif buffer[0] == '06':  # 读取脉冲 FF060000FF读取脉冲1号  FF060100FF读取脉冲2号
        if buffer[1] == '00':
            Speed1 = XRservo.XiaoRGEEK_SpeedCounter1()
            print 'Read_Voltage %d ' % Speed1
        elif buffer[1] == '01':
            Speed2 = XRservo.XiaoRGEEK_SpeedCounter2()
            print 'Read_Voltage %d ' % Speed2
        else:
            print 'error3 command!'
    else:
        print 'error4 command!'


init_light()

# 定义TCP服务器相关变量
HOST = ''
PORT = 2001
BUFSIZ = 1
ADDR = (HOST, PORT)
rec_flag = 0
i = 0
buffer = []
# 启动TCP服务器，监听2001端口
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(1)

threads = []
t1 = threading.Thread(target=Cruising_Mod, args=(u'模式切换',))
threads.append(t1)
t2 = threading.Thread(target=Path_Dect_img_processing, args=(u'图像处理',))
threads.append(t2)

for t in threads:
    t.setDaemon(True)
    t.start()
    print 'theads stat...'
print 'all theads stat...'
while True:
    print 'waitting for connection...'
    tcpCliSock, addr = tcpSerSock.accept()
    print '...connected from:', addr
    while True:
        try:
            data = tcpCliSock.recv(BUFSIZ)
            data = binascii.b2a_hex(data)
        except:
            print "Error receiving:"
            break

        if not data:
            break
        if rec_flag == 0:
            if data == 'ff':
                buffer[:] = []
                rec_flag = 1
                i = 0
        else:
            if data == 'ff':
                rec_flag = 0
                if i == 3:
                    print 'Got data', str(buffer)[1:len(str(buffer)) - 1], "\r"
                    Communication_Decode();
                i = 0
            else:
                buffer.append(data)
                i += 1

            # print(binascii.b2a_hex(data))
    tcpCliSock.close()
Motor_Stop()
tcpSerSock.close()
