# coding:utf-8
'''
Raspberry Pi Car Demo Series
'''
import time
import threading
import cv2
import pygame
import car_agent

# from car_agent import Cars

"""
    Motor Control Deom
    A demo for motor contorl with camera real-time displaying
    
"""

is_capture_running = False
video_capture = cv2.VideoCapture(0)

def pi_capture():
    global is_capture_running, video_capture

    # init the train_label array
    print("Start capture")
    is_capture_running = True

    while is_capture_running:
        #print "reading image..."
        ret, img_frame = video_capture.read()
        #print "reading image done"
        img_frame = cv2.resize(img_frame, (320, 200))
        cv2.imshow('frame', img_frame)

        # sleep for a while and wait to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    print "Stop capture"


class MotorControlDemp:
    def __init__(self):
        pass

    def controlling(self):
        global is_capture_running

        # init pygame parameters
        pygame.init()
        pygame.display.set_mode((100, 100))
        car = Cars()
        # motor_agent.stop

        time.sleep(0.1)

        print "Start to control the car(w,s,a,d)"

        while is_capture_running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    key_input = pygame.key.get_pressed()

                    if key_input[pygame.K_w]:
                        print "Forward"
                        car.go_forward()
                    elif key_input[pygame.K_a]:
                        print "Left"
                        car.turn_left()
                        time.sleep(0.1)
                    elif key_input[pygame.K_d]:
                        print "Right"
                        car.turn_right()
                        time.sleep(0.1)
                    elif key_input[pygame.K_s]:
                        print "Backward"
                        car.go_backward()
                    elif key_input[pygame.K_k]:
                        car.stop()
                        print "Stop K"
                        is_capture_running = False

                # elif event.type == pygame.KEYUP:
                #     key_input = pygame.key.get_pressed()

                #     if key_input[pygame.K_w] and not key_input[pygame.K_a] and not key_input[pygame.K_d]:
                #         print "Forward Up"
                #         # zth_car_control.go_forward()

                #     elif key_input[pygame.K_s] and not key_input[pygame.K_a] and not key_input[pygame.K_d]:
                #         print "Backward Up"
                #         # zth_car_control.go_backward()
                #     else:
                #         print "Stop \n"
                #         # zth_car_control.stop()
            pass


if __name__ == '__main__':
    demo = MotorControlDemp()

    #capture_thread = threading.Thread(target=pi_capture, args=())  # 开启线程
    #capture_thread.setDaemon(True)
    #capture_thread.start()

    #pi_capture()
    is_capture_running = True

    demo.controlling()
