# coding:utf-8
'''
Raspberry Pi Car Demo Series
'''
import time
import threading
import cv2
import pygame
import sys
sys.path.append('../model/')
import cars_agent
import train_control_model

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
        self.is_collect_data = False
        self.save_image_path = '../../data/raw'

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
            img_frame = cv2.cvtColor(img_frame, cv2.COLOR_BGR2GRAY) # set image to gray, reduce color noise
            cv2.imshow('frame', img_frame) # render image frame to window

            key = cv2.waitKey(1) # read keyboard press within 1ms

            train_label = "null"

            # sleep for a while and wait to quit
            if key & 0xFF == ord('w'):
                self.car_agent.forward()
                print "I:Foward"
                train_label = "forward"
            elif key & 0xFF == ord('s'):
                self.car_agent.backward()
                print "I:Backward"
                train_label = "backward"
            elif key & 0xFF == ord('a'):
                self.car_agent.left()
                print "I:GoLeft"
                train_label = "left"
            elif key & 0xFF == ord('d'):
                self.car_agent.right()
                print "I:GoRight"
                train_label = "right"
            elif key & 0xFF == ord('q'):
                self.car_agent.stop()
                print "I:Stop"
                train_label = "stop"
            elif key & 0xFF == ord('p'):
                self.is_capture_running = False
                self.car_agent.stop()
                print "Quiting..."
                break

            if self.is_collect_data:
                ts = str(int(time.time()))
                img_path = "%s/%s_%s.png" % (self.save_image_path, ts, train_label)
                cv2.imwrite(img_path, img_frame)
                print "  -> write raw image: %s" % img_path


    def run_auto_mode(self, model_path):
        control_model = train_control_model.ControlModel('')
        control_model.load_model(model_path)

        while True:
            # capture image from webcam live steam
            ret, img_frame = self.video_capture.read()
            img_frame = cv2.resize(img_frame, (self.cam_width, self.cam_height))
            #img_frame = cv2.cvtColor(img_frame, cv2.COLOR_BGR2GRAY) # set image to gray, reduce color noise
            cv2.imshow('frame', img_frame) # render image frame to window

            pred = control_model.predict(img_frame)

            if pred == 0:
                self.car_agent.stop()
                print "A:Stop"
            elif pred == 1:
                self.car_agent.left()
                print "A:Left"
            elif pred == 2:
                self.car_agent.right()
                print "A:Right"
            elif pred == 3:
                self.car_agent.forward()
                print "A:Forward"
            elif pred == 4:
                self.car_agent.backward()
                print "A:Backward"

            key = cv2.waitKey(1) # read keyboard press within 1ms

            # sleep for a while and wait to quit
            if key & 0xFF == ord('p'):
                print "Quiting auto mode..."
                break

if __name__ == '__main__':
    demo = MotorControlDemp()

    # collect mode
    if len(sys.argv) > 1 and sys.argv[1] == "collect":
        demo.is_collect_data = True
        demo.run_and_capture()

    # auto tracking path mode
    if len(sys.argv) > 2 and sys.argv[1] == "auto":
        demo.run_auto_mode(sys.argv[2])
