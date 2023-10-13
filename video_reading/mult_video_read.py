import numpy as np
import cv2

video_path = r'D:\opencv\video_reading\photoimage\video.mp4'

cap = cv2.VideoCapture(video_path)

while cap.isOpened():
	ret, frame = cap.read()
	if ret:
		frame = cv2.resize(frame,(600,400))

		frame_2 = np.hstack((frame,frame))
		frame_4 = np.vstack((frame_2,frame_2))

		cv2.imshow("Video Playing",frame_4)
		if cv2.waitKey(25) & 0xff == ord('q'):
			break
	else:
		break

cap.release()
cv2.destroyAllWindows()

# import cv2

# cap = cv2.VideoCapture(0)

# def rescale_frame(frame, percent=75):
#     width = int(frame.shape[1] * percent/ 100)
#     height = int(frame.shape[0] * percent/ 100)
#     dim = (width, height)
#     return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)

# while True:
#     rect, frame = cap.read()
#     frame75 = rescale_frame(frame, percent=75)
#     cv2.imshow('frame75', frame75)
#     # frame150 = rescale_frame(frame, percent=150)
#     # cv2.imshow('frame150', frame150)

# cap.release()
# cv2.destroyAllWindows()