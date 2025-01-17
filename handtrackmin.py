import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

cTime = 0
pTime = 0

while True:
    success, img = cap.read()
    # as mphand only works in rgb images hence convert it
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(imgRGB)
    #print(result.multi_hand_landmarks)

    if result.multi_hand_landmarks:
        for handsLms in result.multi_hand_landmarks:
            for id, lm in enumerate(handsLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)

            mpDraw.draw_landmarks(img, handsLms, mpHands.HAND_CONNECTIONS)
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (57, 255, 20), 4)
    cv2.imshow("image", img)
    cv2.waitKey(1)
