# coding:utf-8
'''
Raspberry Pi Car Demo Series
'''
import time
import threading
import cv2
import pygame
import sys
import cars_agent

# from car_agent import Cars

"""
    Motor Control Deom
    A demo for motor contorl with camera real-time displaying

"""

is_capture_running = False

class MotorControlDemp:
    def __init__(self):
        self.car_agent = cars_agent.Cars()

        self.is_capture_running = True

        self.video_capture = cv2.VideoCapture(0)
        self.cam_width = 120
        self.cam_height = 80

        print "=== Initalization Done ==="
        pass

    def run_and_capture(self):
        while self.is_capture_running:
            # capture image from webcam live steam
            ret, img_frame = self.video_capture.read()
            img_frame = cv2.resize(img_frame, (self.cam_width, self.cam_height))
            cv2.imshow('frame', img_frame) # render image frame to window

            key = cv2.waitKey(1) # read keyboard press within 1ms

            # sleep for a while and wait to quit
            if key & 0xFF == ord('w'):
                self.car_agent.forward()
                print "I:Foward"
            elif key & 0xFF == ord('s'):
                self.car_agent.backward()
                print "I:Backward"
            elif key & 0xFF == ord('a'):
                self.car_agent.left()
                print "I:GoLeft"
            elif key & 0xFF == ord('d'):
                self.car_agent.right()
                print "I:GoRight"
            elif key & 0xFF == ord('q'):
                self.car_agent.stop()
                print "I:Stop"
            elif key & 0xFF == ord('p'):
                self.is_capture_running = False
                self.car_agent.stop()
                print "Quiting..."
                break



if __name__ == '__main__':
    demo = MotorControlDemp()
    demo.run_and_capture()

