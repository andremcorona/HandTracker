import cv2
import mediapipe as mp
import time
import HandConversion as hc

class handDetector():

    #####################################################
    #    def __init__()                                 #
    #####################################################
    def __init__(self):

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils

    #####################################################
    #    def findHands()                                #
    #    This function is used to locate any hands      #
    #    that appear in the img and draw them.          # 
    #####################################################
    def findHands(self, img, draw = True):

        # Reflect the image to resemble a mirror
        img = cv2.flip(img, flipCode=1)

        # Convert the BGR image to RGB since mp requires RGB input for processing
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Process the img using mp's hand detection model
        self.results = self.hands.process(imgRGB)

        # If any hand landmarks are detected, loop through each hand's landmarks
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        
        return img
    
    #####################################################
    #    def findPosition()                             #
    #    This function is used locate the points all    #
    #    the hand landmarks and return a dictionary     # 
    #    for both of the hands.                         #
    #####################################################
    def findPosition(self, img): 

        # Initialize landmarks for both hands
        lefthandDict = {}
        rightHandDict = {}
        
        # Only proceed if any hand landmarks are detected
        if self.results.multi_hand_landmarks:

            # Iterate over detected hands
            for handID, handLms in enumerate(self.results.multi_hand_landmarks):

                # Retrieve left or right hand label
                label = self.results.multi_handedness[handID].classification[0].label
            
                for id, lm in enumerate(handLms.landmark):

                    # Retrive height, width and center of image
                    h, w, c = img.shape

                    # Calulate coordinates of the landmark
                    cx, cy = int(lm.x*w), int(lm.y*h)

                    # Store landmarks and their coordinates in dictionary
                    if label == "Left": lefthandDict[id] = [cx, cy]
                    if label == "Right": rightHandDict[id] = [cx, cy]

                    # Draw the specified landmarks
                    if id == 0 or id == 4 or id == 8 or id == 12 or id == 16 or id == 20:
                        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
        
        # Return a dictionary for each hand
        return lefthandDict, rightHandDict 

def main():
    # Initialize prev and current time variables for FPS counter
    pTime = 0
    cTime = 0

    # Open the default webcam
    cap = cv2.VideoCapture(0)

    # Create an instance of the handDetector class
    detector = handDetector()

    while True:
        # Capture a frame from the webcam
        success, img = cap.read()

        # Pass the fram to the hand detector
        img = detector.findHands(img)

        # Get the positions of both hands using the findPosition function
        leftHandDict, rightHandDict = detector.findPosition(img)

        # OPTIONAL: Take finger count for fun
        hc.takeCount(img, leftHandDict, rightHandDict)

        # Calculate the current FPS
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        # Overlay the FPS value
        cv2.putText(img, str(int(fps)), (5,40), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 3)

        # Display the proccessed video to a window
        cv2.imshow("Live Camera", img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()