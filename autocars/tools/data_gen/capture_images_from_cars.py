import os
import cv2
import time
import numpy as np

from dnn_model import DNNModel

model = DNNModel(None)
cap = cv2.VideoCapture(0)

label = 1 # left is default

cnt_l = 0
cnt_r = 0

while cap.isOpened():
    k = cv2.waitKey(1) & 0xFF
    if k == ord('q'):
        break
    if k == ord('p'):
        continue

    if k == ord('l'):
        label = 1

    if k == ord('r'):
        label = 2l
        cnt_r += 1

    print "l=%d\tr=%d" % (cnt_l, cnt_r)

    if label == 1:
        cnt_l += 1
    else:
        cnt_r += 1


    #print cap
    ret, frame = cap.read()

    frame = cv2.resize(frame, (64, 64))

    model.add_training_sample(frame, label)

    cv2.imshow('frame',frame)

    time.sleep(0.01)

cap.release()
cv2.destroyAllWindows()

print len(model.data)
model.scale_and_norm_training_samples()
model.train()
model.test()

model.save_model()