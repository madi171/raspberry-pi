#!/usr/bin/env python
# -*- coding: utf-8 -*-

from VideoCapture import Device
import time
import sys, pygame

pygame.init()

size = width, height = 620, 485
speed = [2, 2]
black = 0, 0, 0

pygame.display.set_caption('视频窗口@dyx1024')
screen = pygame.display.set_mode(size)

#抓取频率，抓取一次
SLEEP_TIME_LONG = 0.1

#初始化摄像头
cam = Device(devnum=0, showVideoWindow=0)

while True:

    #抓图
    cam.saveSnapshot('test.jpg', timestamp=3, boldfont=1, quality=75)

    #加载图像
    image = pygame.image.load('test.jpg')

    #传送画面
    screen.blit(image, speed)

    #显示图像
    pygame.display.flip()
    #休眠一下，等待一分钟
    time.sleep(SLEEP_TIME_LONG)

