import cv2
import pytesseract
from PIL import Image
frameWidth = 640
frameHeight = 480
count = 0
nPlateCascade = cv2.CascadeClassifier('indian_license_plate.xml')
minArea = 200
color = (255,0,255)
cap = cv2.VideoCapture('/home/mtv/Downloads/video_no_plate.mp4')
cap.set(3,frameWidth)
cap.set(4,frameHeight)
cap.set(10,150)
while True:
    success, img = cap.read()
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    numberPlate = nPlateCascade.detectMultiScale(imgGray,1.5,8)
    for (x,y,w,h) in numberPlate:
        area = w*h
        if area > minArea:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            cv2.putText(img,"Number Plate",(x,y-5),cv2.FONT_HERSHEY_SIMPLEX,1,color,2)
            imgRoi = img[y:y+h,x:x+w]
            cv2.imshow("ROI",imgRoi)
            # img1 = cv2.imread(img)
            color_coverted = cv2.cvtColor(imgRoi, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(color_coverted)
            # pil_image.show()
            img2 = cv2.resize(color_coverted, (640, 480))
            d = pytesseract.image_to_data(img2)
            print(d)
    cv2.imshow("Result",img)
    if cv2.waitKey(1) & 0xFF == ord('s'):
        cv2.imwrite(str(count) + ".jpg", imgRoi)
        cv2.rectangle(img,(0,200),(640,300),(0,255,0),cv2.FILLED)
        cv2.putText(img,"Scan Saved",(150,265),cv2.FONT_HERSHEY_DUPLEX,2,(0,0,255),2)
        cv2.imshow("Result",img)
        cv2.waitKey(500)
        count +=1










