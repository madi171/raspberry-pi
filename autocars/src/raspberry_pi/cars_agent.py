# coding:utf-8
import sys
import os
import cv2
import time
import numpy as np
import RPi.GPIO as GPIO

'''
Cars is the agent of vehicle, it contains many functions to control the cars

    Car motor directions:
      ENB                ENA 
    
      IN3   | ------- |  IN1      
                 |
                 | 
                 |
                 |
      IN4   | ------- |  IN2

    IN1, IN3 1 - > UP  0 -> DOWN
    IN2, IN4 0 - > UP  1 -> DOWN

'''
class Cars:

    def __init__(self):
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
        Motor speed define
        '''
        self.VIECLE_SPEED_HIGH = 80 # high speed
        self.VIECLE_SPEED_LOW = 40 # low speed

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
        Motor init to set to default freq and speed
        '''
        GPIO.setup(self.ENA, GPIO.OUT, initial=GPIO.LOW)
        self.ENA_pwm = GPIO.PWM(self.ENA, 1000)
        self.ENA_pwm.start(0)
        self.ENA_pwm.ChangeDutyCycle(100)
        GPIO.setup(self.IN1, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.IN2, GPIO.OUT, initial=GPIO.LOW)

        GPIO.setup(self.ENB, GPIO.OUT, initial=GPIO.LOW)
        self.ENB_pwm = GPIO.PWM(self.ENB, 1000)
        self.ENB_pwm.start(0)
        self.ENB_pwm.ChangeDutyCycle(100)
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


    def set_speed(self, speed_rate):
        self.ENA_pwm.ChangeDutyCycle(speed_rate)
        self.ENB_pwm.ChangeDutyCycle(speed_rate)


    def go_forward(self):
        print 'motor_forward'
        GPIO.output(self.ENA, True)
        GPIO.output(self.ENB, True)
        GPIO.output(self.IN1, True)
        GPIO.output(self.IN2, False)
        GPIO.output(self.IN3, True)
        GPIO.output(self.IN4, False)
        GPIO.output(self.LED1, False)  # LED1亮
        GPIO.output(self.LED2, False)  # LED1亮
        self.set_speed(self.VIECLE_SPEED_HIGH)

    def go_backward(self):
        print 'motor_backward'
        GPIO.output(self.ENA, True)
        GPIO.output(self.ENB, True)
        GPIO.output(self.IN1, False)
        GPIO.output(self.IN2, True)
        GPIO.output(self.IN3, False)
        GPIO.output(self.IN4, True)
        GPIO.output(self.LED1, True)  # LED1灭
        GPIO.output(self.LED2, False)  # LED2亮
        self.set_speed(self.VIECLE_SPEED_HIGH)

    def turn_left(self):
        print 'motor_turnleft'
        GPIO.output(self.ENA, True)
        GPIO.output(self.ENB, True)
        GPIO.output(self.IN1, True)
        GPIO.output(self.IN2, False)
        GPIO.output(self.IN3, False)
        GPIO.output(self.IN4, True)
        GPIO.output(self.LED1, False)  # LED1亮
        GPIO.output(self.LED2, True)  # LED2灭
        self.set_speed(self.VIECLE_SPEED_LOW)

    def turn_right(self):
        print 'motor_turnright'
        GPIO.output(self.ENA, True)
        GPIO.output(self.ENB, True)
        GPIO.output(self.IN1, False)
        GPIO.output(self.IN2, True)
        GPIO.output(self.IN3, True)
        GPIO.output(self.IN4, False)
        GPIO.output(self.LED1, False)  # LED1亮
        GPIO.output(self.LED2, True)  # LED2灭
        self.set_speed(self.VIECLE_SPEED_LOW)

    def stop(self):
        print 'motor_stop'
        GPIO.output(self.ENA, False)
        GPIO.output(self.ENB, False)
        GPIO.output(self.IN1, False)
        GPIO.output(self.IN2, False)
        GPIO.output(self.IN3, False)
        GPIO.output(self.IN4, False)
        GPIO.output(self.LED1, True)  # LED1灭
        GPIO.output(self.LED2, True)  # LED2亮

