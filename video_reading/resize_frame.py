import cv2
  

video_path = r'D:\opencv\video_reading\photoimage\video1.mp4'

# Define a video capture object
vidcap = cv2.VideoCapture(video_path)
  
# Capture video frame by frame
success, image = vidcap.read()
  
# Declare the variable with value 0
count = 0
  
# Creating a loop for running the video
# and saving all the frames
while success:
  
    # Capture video frame by frame
    success, image = vidcap.read()
  
    # Resize the image frames
    resize = cv2.resize(image, (1980, 1200))
  
    # Saving the frames with certain names
    cv2.imwrite("%04d.jpg" % count, resize)
  
    # Closing the video by Escape button
    if cv2.waitKey(50) == 27:
        break
  
    # Incrementing the variable value by 1
    count += 1