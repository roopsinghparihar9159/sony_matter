import numpy as np
import cv2

video_path = r'D:\opencv\video_reading\photoimage\video.mp4'

cap = cv2.VideoCapture(video_path)

while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        images = cv2.resize(frame,(1200,720))
        cv2.imshow("Video Playing",images)
        if cv2.waitKey(25) & 0xff == ord('q'):
            break
    else:
        break
cap.releas()
cv2.destroyAllWindows()
