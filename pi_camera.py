# coding:utf-8
'''
Raspberry Pi Car Demo Series
'''
import os
import cv2
import time
import numpy as np
import RPi.GPIO as GPIO
from dnn_model import DNNModel
"""
    PiCameraClassication
    A demo for pi-car following object detected by DNN model
    
"""
class PiCameraClassication:
    def __init__(self):
        self.model = DNNModel(None)
        self.model.load_model("greenball_squeezenet.h5")

        if self.model is not None:
            print "Successfully load model."
        else:
            print "Error loading model."
            exit(1)

        self.cap = cv2.VideoCapture(0)
        print "start to capture image frame..."

        '''
        BCM mode set
        '''
        GPIO.setmode(GPIO.BCM)

        '''
        LED const define
        '''
        self.LED0 = 10
        self.LED1 = 9
        self.LED2 = 25

        '''
        Motor const define
        '''
        self.ENA = 13  # //L298使能A
        self.ENB = 20  # //L298使能B
        self.IN1 = 19  # //电机接口1
        self.IN2 = 16  # //电机接口2
        self.IN3 = 21  # //电机接口3
        self.IN4 = 26  # //电机接口4

        '''
        Supersonic const define
        '''
        self.ECHO = 4  # 超声波接收脚位
        self.TRIG = 17  # 超声波发射脚位

        '''
        IR const define
        '''
        self.IR_R = 18  # 小车右侧巡线红外
        self.IR_L = 27  # 小车左侧巡线红外
        self.IR_M = 22  # 小车中间避障红外
        self.IRF_R = 23  # 小车跟随右侧红外
        self.IRF_L = 24  # 小车跟随左侧红外

        GPIO.setwarnings(False)

        '''
        LED light init
        '''
        GPIO.setup(self.LED0, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self.LED1, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self.LED2, GPIO.OUT, initial=GPIO.HIGH)

        '''
        Motor init
        '''
        GPIO.setup(self.ENA, GPIO.OUT, initial=GPIO.LOW)
        ENA_pwm = GPIO.PWM(self.ENA, 1000)
        ENA_pwm.start(0)
        ENA_pwm.ChangeDutyCycle(100)
        GPIO.setup(self.IN1, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.IN2, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.ENB, GPIO.OUT, initial=GPIO.LOW)
        ENB_pwm = GPIO.PWM(self.ENB, 1000)
        ENB_pwm.start(0)
        ENB_pwm.ChangeDutyCycle(100)
        GPIO.setup(self.IN3, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.IN4, GPIO.OUT, initial=GPIO.LOW)

        '''
        Infrared Ray detector init
        '''
        GPIO.setup(self.IR_R, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.IR_L, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.IR_M, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.IRF_R, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.IRF_L, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        '''
        Supersonic detector init
        '''
        GPIO.setup(self.TRIG, GPIO.OUT, initial=GPIO.LOW)  # 超声波模块发射端管脚设置trig
        GPIO.setup(self.ECHO, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # 超声波模块接收端管脚设置echo
        pass

    def Motor_Forward(self):
        print 'motor forward'
        GPIO.output(self.ENA, True)
        GPIO.output(self.ENB, True)
        GPIO.output(self.IN1, True)
        GPIO.output(self.IN2, False)
        GPIO.output(self.IN3, True)
        GPIO.output(self.IN4, False)
        GPIO.output(self.LED1, False)  # LED1亮
        GPIO.output(self.LED2, False)  # LED1亮

    def Motor_Backward(self):
        print 'motor_backward'
        GPIO.output(self.ENA, True)
        GPIO.output(self.ENB, True)
        GPIO.output(self.IN1, False)
        GPIO.output(self.IN2, True)
        GPIO.output(self.IN3, False)
        GPIO.output(self.IN4, True)
        GPIO.output(self.LED1, True)  # LED1灭
        GPIO.output(self.LED2, False)  # LED2亮

    def Motor_TurnLeft(self):
        print 'motor_turnleft'
        GPIO.output(self.ENA, True)
        GPIO.output(self.ENB, True)
        GPIO.output(self.IN1, True)
        GPIO.output(self.IN2, False)
        GPIO.output(self.IN3, False)
        GPIO.output(self.IN4, True)
        GPIO.output(self.LED1, False)  # LED1亮
        GPIO.output(self.LED2, True)  # LED2灭

    def Motor_TurnRight(self):
        print 'motor_turnright'
        GPIO.output(self.ENA, True)
        GPIO.output(self.ENB, True)
        GPIO.output(self.IN1, False)
        GPIO.output(self.IN2, True)
        GPIO.output(self.IN3, True)
        GPIO.output(self.IN4, False)
        GPIO.output(self.LED1, False)  # LED1亮
        GPIO.output(self.LED2, True)  # LED2灭

    def Motor_Stop(self):
        print 'motor_stop'
        GPIO.output(self.ENA, False)
        GPIO.output(self.ENB, False)
        GPIO.output(self.IN1, False)
        GPIO.output(self.IN2, False)
        GPIO.output(self.IN3, False)
        GPIO.output(self.IN4, False)
        GPIO.output(self.LED1, True)  # LED1灭
        GPIO.output(self.LED2, True)  # LED2亮

    def process_single_frame(self):
        print "reading image..."
        ret, img_frame = self.cap.read()
        print "reading image done"

        img_frame = cv2.resize(img_frame, (self.model.IMAGE_SIZE, self.model.IMAGE_SIZE))

        print "predicting image..."
        action_opt = np.argmax(self.model.predict(img_frame))
        print "predict done"

        if action_opt == 0:
            # stop
            self.Motor_Stop()
        elif action_opt == 1:
            # left
            self.Motor_TurnLeft()
            time.sleep(0.01)
        elif action_opt == 2:
            # right
            self.Motor_TurnRight()
            time.sleep(0.01)
        else:
            self.Motor_Stop()
        pass

    def run(self):
        while xrange(20):
            self.process_single_frame()

if __name__ == '__main__':
    demo = PiCameraClassication()
    demo.run()
