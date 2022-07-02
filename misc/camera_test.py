import pygame.camera
import pygame.image
import sys
import time

pygame.init()
pygame.camera.init()

cameras = pygame.camera.list_cameras()
SIZE=(176,144)
webcam = pygame.camera.Camera(cameras[0], SIZE)
#webcam = pygame.camera.Camera(cameras[0])
webcam.start()

screen = pygame.display.set_mode((SIZE[0], SIZE[1]))
pygame.display.set_caption("pygame")

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            sys.exit()
        img = webcam.get_image()
        screen.blit(img, (0,0))
        pygame.display.update()
        time.sleep(0.1)
