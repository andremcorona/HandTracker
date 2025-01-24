import cv2
import math


########################################################
#    This file will be used to create and store        #
#    functions that will recognize finger patterns,    #
#    gestures or whatever it might be we are trying    #
#    to find.                                          #
########################################################

#-----------------------------------------------------------------------------------------------------------------------------------------#

#####################################################
#    def lmsToPos()                                 #
#    This function is used to determine how many    #
#    fingers are pointed in the upright position.   # 
#    Will return all five fingers as a list.        #
#####################################################

def lmsToPos(handDict):

    # List for each finger and its value of being open/closed
    fingersPos = []

    # List of Tip IDs excluding thumb
    tipIds = [8, 12, 16, 20]

    # Run if there are values in dictionary
    if len(handDict) != 0:
        
        # Calculate the distance between thumb and base of pinky
        # Uses two points on the thumb
        fourToSTen = math.hypot(handDict[17][0] - handDict[4][0], handDict[17][1] - handDict[4][1])
        threeToSTen = math.hypot(handDict[17][0] - handDict[2][0], handDict[17][1] - handDict[2][1])

        # Calculate if thumb is extended
        if fourToSTen > threeToSTen:
            fingersPos.append(1)
        else:
            fingersPos.append(0)

        # Compare two y-points on a finger to determine if its extended
        for fingerPoint in range(0, 4):

            # Calculate the distance between a finger tip and base of palm
            # Need a point on the finger to compare to
            tipToSTen = math.hypot(handDict[0][0] - handDict[tipIds[fingerPoint]][0], handDict[0][1] - handDict[tipIds[fingerPoint]][1])
            pointToSTen = math.hypot(handDict[0][0] - handDict[tipIds[fingerPoint] - 2][0], handDict[0][1] - handDict[tipIds[fingerPoint] - 2][1])
            
            # Calculate if the finger is extended
            if tipToSTen > pointToSTen:
                fingersPos.append(1)
            else:
                fingersPos.append(0)

    return fingersPos

#####################################################
#    def takeCount()                                #
#    This function is used to take the count of     #
#    two hands using their dictionaries.            #
#####################################################

def takeCount(img, leftHandDict, rightHandDict):

        leftHand = lmsToPos(leftHandDict)
        rightHand = lmsToPos(rightHandDict)
        totalCount = sum(leftHand + rightHand)

        cv2.putText(img, str(f'Left Hand: {sum(leftHand)}'), (7,375), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 3)
        cv2.putText(img, str(f'Right Hand: {sum(rightHand)}'), (7,400), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 3)
        cv2.putText(img, str(f'Total: {totalCount}'), (7,425), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 3)