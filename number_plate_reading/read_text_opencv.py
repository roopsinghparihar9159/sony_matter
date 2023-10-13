# import cv2
# import pytesseract
# img = cv2.imread("image_text.jpg")
# img = cv2.resize(img,(640,480))
# d = pytesseract.image_to_data(img)
# print(d)
# cv2.imshow('IMG',img)
# cv2.waitKey(0)

import cv2
from PIL import Image

# Open image using openCV2
opencv_image = cv2.imread("image_text.jpg")

# Notice the COLOR_BGR2RGB which means that the color is
# converted from BGR to RGB
color_coverted = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2RGB)
print(color_coverted)

# Displaying the Scanned Image by using cv2.imshow() method
cv2.imshow("OpenCV Image", opencv_image)

# Displaying the converted image
pil_image = Image.fromarray(color_coverted)
pil_image.show()

# waits for user to press any key
# (this is necessary to avoid Python kernel form crashing)
cv2.waitKey(0)

# closing all open windows
cv2.destroyAllWindows()