import cv2
import threading

cap = cv2.VideoCapture(0)

def webcam():
    global cap
    while(True):
        ret, frame = cap.read()
        img = cv2.resize(frame, (176, 144))
        cv2.imshow('frame', img)

        key = cv2.waitKey(1)

        if key & 0xFF == ord('w'):
            print "w"
        elif key & 0xFF == ord('s'):
            print "s"
        elif key & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break


t = threading.Thread(target=webcam, name='LoopThread')
t.start()
t.join()

