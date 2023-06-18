import numpy as np
import cv2
from PIL import Image

img = cv2.imread('shapes2.png')
image = cv2.imread('shapes2.png')
imgGrey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, thrash = cv2.threshold(imgGrey, 50, 255, cv2.THRESH_BINARY)
contours, _ = cv2.findContours(thrash, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

# in BGR mode
red = [36, 28, 237]
blue = [255, 0, 0]
green = [0, 255, 0]
yellow = [38, 206, 255]
orange = [42, 136, 255]
pink = [192, 88, 165]



cv2.imshow("img", img)

def get_limits(color):

    c = np.uint8([[color]])  # here insert the bgr values which you want to convert to hsv
    hsvC = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)

    lowerLimit = hsvC[0][0][0] - 10, 100, 100
    upperLimit = hsvC[0][0][0] + 10, 255, 255

    lowerLimit = np.array(lowerLimit, dtype=np.uint8)
    upperLimit = np.array(upperLimit, dtype=np.uint8)

    return lowerLimit, upperLimit

def controlColor(hsvImage, color, colorName, prevColorName):
    
    if prevColorName != "":
        return prevColorName

    lowerLimit, upperLimit = get_limits(color=color)

    mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)

    mask_ = Image.fromarray(mask)

    bbox = mask_.getbbox()
    
    if bbox is not None:
        return colorName
    return ""
    

for contour in contours:

    approx = cv2.approxPolyDP(contour, 0.01* cv2.arcLength(contour, True), True)
    cv2.drawContours(img, [approx], 0, (0, 0, 0), 5)
    x = approx.ravel()[0]
    y = approx.ravel()[1] - 5
    x1 ,y1, w, h = cv2.boundingRect(approx)
    x2, y2 = x1+w, y1+h
    ROI = image[y:y2, x:x2]
    hsvImage = cv2.cvtColor(ROI, cv2.COLOR_BGR2HSV)
    cv2.rectangle(img, (x1,y1), (x1 + w, y1 + h), (0, 0, 255), 3)
   
    colorName = controlColor(hsvImage, green , "green", "")
    colorName = controlColor(hsvImage, red, "red", colorName)
    colorName = controlColor(hsvImage, blue, "blue", colorName)
    colorName = controlColor(hsvImage, yellow, "yellow", colorName)
    colorName = controlColor(hsvImage, orange, "orange", colorName)
    colorName = controlColor(hsvImage, pink, "pink", colorName)
    

    if len(approx) == 3:
        cv2.putText(img, "Triangle " + colorName, (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255))
    elif len(approx) == 4:
        x1 ,y1, w, h = cv2.boundingRect(approx)
        aspectRatio = float(w)/h
        print(aspectRatio)
        if aspectRatio >= 0.90 and aspectRatio <= 1.10:
          cv2.putText(img, "square " + colorName, (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255))
        else:
          cv2.putText(img, "rectangle " + colorName, (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255))
    elif len(approx) == 5:
        cv2.putText(img, "Pentagon " + colorName, (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255))
    elif len(approx) == 10:
        cv2.putText(img, "Star " + colorName, (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255))
    else:
        cv2.putText(img, "Circle " + colorName, (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255))


cv2.imshow("shapes", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
