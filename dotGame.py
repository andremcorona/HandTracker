import cv2
import HandTracker as ht
import HandConversion as hc
import random

########################################################
#    This file is playable on its own but I built it   #
#    with the intent of using it in the HandTracking-  #
#    Game file. Which will consist of other games.     #
########################################################

# Setup camera dimensions
wCam, hCam = 640, 480
#gameTime = 60

# Initialize the camera
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

# Initialize the hand detector
detector = ht.handDetector()

#####################################################
#    def dotGenerator()                             #
#    This function is the very core of the dotGame  #
#    as it will generate a new location for the     # 
#    dot whenever it is pressed and controls any    #
#    other elements of the game.                    #
#####################################################

def dotGenerator(img, rightHandDict, gameOn, dotx, doty, counter):
    # Variables
    bubblex, bubbley = wCam - 40, 40
    endx, endy = wCam - 40, 120

    # If game is not started, place a start bubble in top right corner
    if not gameOn:
        cv2.circle(img, (bubblex, bubbley), 40, (177, 150, 177), cv2.FILLED)
        cv2.putText(img, str(f'DOT'),  (bubblex - 15, bubbley + 5), cv2.FONT_HERSHEY_PLAIN, 1,(255, 255, 255), 1)

    # Check if the hand is detected as the program depends on this to work
    if len(rightHandDict) != 0:
        # If the start bubble is touched by the index finger, start the game
        if abs(rightHandDict[8][0] - bubblex) < 10 and abs(rightHandDict[8][1] - bubbley) < 10:
            gameOn = True

        # Gernerate circles during game and reset game if ended
        if gameOn:
            cv2.circle(img, (dotx, doty), 20, (177, 150, 177), cv2.FILLED)
            if abs(rightHandDict[8][0] - dotx) < 10 and abs(rightHandDict[8][1] - doty) < 10:
                dotx, doty = random.randint(20, wCam - 20), random.randint(20, hCam - 20)
                counter += 1
            
            cv2.circle(img, (endx, endy), 40, (177, 150, 177), cv2.FILLED)
            cv2.putText(img, str(f'END'), (endx - 15, endy + 5), cv2.FONT_HERSHEY_PLAIN, 1,(255, 255, 255), 1)
            if abs(rightHandDict[8][0] - endx) < 10 and abs(rightHandDict[8][1] - endy) < 10:
                counter = 0
                gameOn = False

            # Overlay the point value
            cv2.putText(img, str(f'POINTS: {counter}'), (5,40), cv2.FONT_HERSHEY_PLAIN, 2,(177, 150, 177), 3)

    # Return variables
    return gameOn, dotx, doty, counter


def main():
    # Global Variables
    counter = 0
    gameOn = False

    # Give first dot an initial position
    dotx, doty = random.randint(20, wCam - 20), random.randint(20, hCam - 20)

    # Main Loop
    while True:
        # Read frame from camera
        success, img = cap.read()

        # Detect the hands and theirs positions
        img = detector.findHands(img)
        leftHandDict, rightHandDict = detector.findPosition(img)

        # Update the game state constantly
        gameOn, dotx, doty, counter = dotGenerator(img, rightHandDict, gameOn, dotx, doty, counter)

        # Display camera feed with game overlay
        cv2.imshow("Camera", img)
        cv2.waitKey(1)

        # Exit the program if the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('c'):
            break

# Run the program if this script is executed directly
if __name__ == "__main__":
    main()