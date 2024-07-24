import cv2
import numpy as np
import time
import os
import handtrackingmodule as htm


##############################
brushThickness = 20
eraserThickness = 80
##############################


folderpath = "design"
mylist = os.listdir(folderpath)
print(mylist)
overlayList = []
for imgPath in mylist:
    image = cv2.imread(f'{folderpath}/{imgPath}')
    overlayList.append(image)

header = overlayList[0]
hcolor = (255, 1, 1)
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 650)

detector = htm.handDetector(0.65)
xp, yp = 0, 0

imgCanvas = np.zeros((720, 1280, 3), np.uint8)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    img = detector.findHands(img)
    Lmlist = detector.findPosition(img, draw=False)

    if len(Lmlist) != 0:
        #print(lmlist)
        x1, y1 = Lmlist[8][1:]
        x2, y2 = Lmlist[12][1:]

        #to check which fingers up
        fingers = detector.fingersUp()

        #to check if selection or writing mode
        if fingers[1] and fingers[2]:

            #cv2.rectangle(img, (x1, y1 - 20), (x2, y2 + 20), hcolor, cv2.FILLED)
            if y1 < 140:
                if 108 < x1 < 243:
                    header = overlayList[0]
                    hcolor = (255, 1, 1)
                    #blue
                elif 254 < x1 < 389:
                    header = overlayList[1]
                    hcolor = (1, 1, 255)
                    #red
                elif 400 < x1 < 535:
                    header = overlayList[2]
                    hcolor = (1, 191, 98)
                    #green
                elif 546 < x1 < 681:
                    header = overlayList[3]
                    hcolor = (0,255,255)
                    #yellow

                elif 692 < x1 < 827:
                    header = overlayList[4]
                    hcolor = (255, 103, 197)
                    #pink
                elif 833 < x1 < 973:
                    header = overlayList[5]
                    hcolor = (255, 255, 255)
                    #black
                elif 984 < x1 < 1197:
                    header = overlayList[6]
                    hcolor = (0,0,0)
                    #eraser

            cv2.rectangle(img, (x1, y1 - 20), (x2, y2 + 20), hcolor, cv2.FILLED)
            xp, yp = x1, y1

        if fingers[1] and fingers[2] == False:
            cv2.circle(img, (x1, y1), 15, hcolor, cv2.FILLED)
            print("Drawing Mode")
            if xp == 0 and yp == 0:
                xp, yp = x1, y1


            if hcolor == (0,0,0):
                cv2.line(imgCanvas, (xp, yp), (x1, y1), hcolor, eraserThickness)
                cv2.line(img, (xp, yp), (x1, y1), hcolor, eraserThickness)
                xp, yp = x1, y1
            else:
                cv2.line(img, (xp, yp), (x1, y1), hcolor, brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), hcolor, brushThickness)
                xp, yp = x1, y1

    img[0:140, 0:1280] = header

    img = cv2.addWeighted(img, 0.5, imgCanvas, 0.5, 0)

    cv2.imshow("Image", img)

    cv2.imshow("Canvas", imgCanvas)

    cv2.waitKey(1)
