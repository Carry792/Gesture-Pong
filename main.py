from shutil import which

import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

imgBackground = cv2.imread("Background.png")
imgGameOver = cv2.imread("gameOver.png")
imgBat1 = cv2.imread("bat1.png", cv2.IMREAD_UNCHANGED)
imgBat2 = cv2.imread("bat2.png", cv2.IMREAD_UNCHANGED)
imgBall = cv2.imread("Ball.png", cv2.IMREAD_UNCHANGED)

#Detects hand
detector = HandDetector(detectionCon= 0.8, maxHands=2)

#Initial ball
ballPos = [100, 100]

#x and y speed
speedX = 25
speedY = 25

gameOver = False

score = [0,0]

while True:
    _, img = cap.read()
    img = cv2.flip(img, 1)
    imgRaw = img.copy()

    #hand and landmark finding
    hands, img = detector.findHands(img, flipType= False)


    # Background overlay
    img = cv2.addWeighted(img, 0.2, imgBackground, 0.8, 0)

    #Check hands

    if hands:
        for hand in hands:
            x,y,w,h = hand['bbox']
            h1, w1, _ = imgBat1.shape
            y1 = y - h1//2
            y1 = np.clip(y1, 20, 415)

            if hand['type'] == "Left":
                img = cvzone.overlayPNG(img, imgBat1, (59, y1))
                if 59 < ballPos[0] < 59+w1 and y1 < ballPos[1] < y1+h1:
                    speedX = -speedX
                    ballPos[0] += 30
                    score[0] += 1

            if hand['type'] == "Right":
                img = cvzone.overlayPNG(img, imgBat2, (1195, y1))
                if 1195 - 50 < ballPos[0] < 1199 and y1 < ballPos[1] < y1+h1:
                    speedX = -speedX
                    ballPos[0] -= 30
                    score[1] += 1

    #Game over
    if ballPos[0] < 40 or ballPos[0] > 1200:
        gameOver = True

    if gameOver:
        img = imgGameOver
        cv2.putText(img, str(score[1] + score[0]).zfill(2), (585, 360), cv2.FONT_HERSHEY_COMPLEX, 2.5, (200, 0, 200), 5)

    else:
    #Move the ball
        if ballPos[1] >= 500 or ballPos[1] <= 10:
            speedY = -speedY

        ballPos[0] += speedX
        ballPos[1] += speedY

        #add ball
        img = cvzone.overlayPNG(img, imgBall, ballPos)

        #Display the score
        cv2.putText(img, str(score[0]), (300,650), cv2.FONT_HERSHEY_COMPLEX, 3, (255,255,255), 5)
        cv2.putText(img, str(score[1]), (900, 650), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5)

    img[580:700, 20:233] = cv2.resize(imgRaw, (213, 120))

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)

#reset
    if key == ord('r'):
        ballPos = [100, 100]
        speedX = 15
        speedY = 15
        gameOver = False
        score = [0, 0]
        imgGameOver = cv2.imread("gameOver.png")

