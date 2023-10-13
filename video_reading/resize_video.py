import numpy as np
import cv2

cap = cv2.VideoCapture(0)


def make_1080p():
	cap.set(3,1920)
	cap.set(4,1080)

def make_7200p():
	cap.set(3,1280)
	cap.set(4,720)

def make_480p():
	cap.set(3,640)
	cap.set(4,480)

def change_res(width, height):
	cap.set(3,width)
	cap.set(4,height)

make_1080p()

while(True):
	ret, frame = cap.read()
	cv2.imshow('Frame',frame)
	if cv2.waitKey(20) & 0xff == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()