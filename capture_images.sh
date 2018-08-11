#!/bin/bash

fswebcam -d /dev/video0 --no-banner -l 1 greenball_right_%H%M%S.jpg

fswebcam -d /dev/video0 --no-banner -l 1 greenball_left_%H%M%S.jpg