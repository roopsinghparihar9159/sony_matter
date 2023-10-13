import numpy as np
import cv2

filename = 'video.avi'
frames_per_secods = 24.0
my_res = '4k'

def change_res(cap,width,height):
	cap.set(3,width)
	cap.set(4,height)

STD_DIMENSIONS = {
	"480p":(640,480),
	"720":(1280,720),
	"1080p":(1920,1080),
	"4k":(3840,2160),
}

def get_dims(cap,res='1080p'):
	width,height = STD_DIMENSIONS['480p']
	if res in STD_DIMENSIONS:
		width,height = STD_DIMENSIONS[res]
	change_res(cap,width,height)
	return width,height

VIDEO_TYPE = {
	'avi':cv2.VideoWriter_fourcc(*'XVID'),
	'mp4':cv2.VideoWriter_fourcc(*'XVID'),
}


def get_video_type(filename):
	filename, ext = os.path.splitext(filename)
	if ext in VIDEO_TYPE:
		return VIDEO_TYPE[ext]
	return VIDEO_TYPE['avi']




cap = cv2.VideoCapture(0)
dims = get_dims(cap, res=my_res)

while(True):
	ret, frame = cap.read()

	cv2.imshow('frame',frame)
	if cv2.waitKey(20) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()