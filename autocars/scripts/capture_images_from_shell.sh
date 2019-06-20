#!/bin/bash

TASK_NAME="obj_follow"
IMG_SIZE="160x120"
LABEL="left"

# usage: -l(loop) secends
fswebcam -d /dev/video0 --no-banner -r ${IMG_SIZE} -l 1 ${TASK_NAME}_${LABEL}_%H%M%S.jpg
