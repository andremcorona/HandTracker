#-------------IN EARLY STAGES-------------#

import cv2
import HandTracking as ht
import HandConversion as hc

wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = ht.handDetector()

while True:
    success, img = cap.read()

    img = detector.findHands(img)
    leftHandDict, rightHandDict = detector.findPosition(img)
    hc.takeCount(img, leftHandDict, rightHandDict)

    cv2.imshow("Camera", img)
    cv2.waitKey(1)