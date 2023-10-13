import numpy as np
import cv2

video_path1 = r'D:\opencv\video_reading\photoimage\video.mp4'
video_path = r'D:\opencv\video_reading\photoimage\video.mp4'

cap = cv2.VideoCapture(video_path1)
while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        image = cv2.resize(frame,(600,400))
        cv2.imshow("Video Player",image)
        if cv2.waitKey(25) & 0xff == ord('q'):
            break
    else:
        break
cap.release()
cv2.destroyAllWindows()
