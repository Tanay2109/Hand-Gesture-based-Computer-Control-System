import cv2 as cv
import os
import time
import HTM1 as htm

cap=cv.VideoCapture(0)
wCam,hCam=680,480
cap.set(3,wCam)
cap.set(4,hCam)
folderPath="Number images"
myList=os.listdir(folderPath) # Number images to display
print(myList)
overLayList=[]
pTime=0
for imPath in myList:
    image=cv.imread(f'{folderPath}/{imPath}')
    if image is not None:
        resized_overlay = cv.resize(image, (200, 200))
        #print(f'{folderPath}/{imPath}')
        overLayList.append(resized_overlay) #Overlaying the images over the webcam video


print(len(overLayList))
detector=htm.handDetector(detectionCon=0.8)

tipIDs=[4,8,12,16,20] # IDs of the finger tips


while True:
    success,img=cap.read()
    img=detector.findHands(img)
    lmList=detector.findPosition(img)
    #print(lmList)

    if len(lmList)!=0:
        fingers=[]

        #Thumb

        if lmList[tipIDs[0]][1] > lmList[tipIDs[0]-1][1]:
                    fingers.append(1)
        else:
          fingers.append(0)

        for id in range(1,5):
                 if lmList[tipIDs[id]][2] < lmList[tipIDs[id]-2][2]:
                    fingers.append(1)
                 else:
                   fingers.append(0)
        #print(fingers)
        totalFingers=fingers.count(1)
        print(totalFingers) # To show the total fingers that are up
        h, w, c = overLayList[totalFingers-1].shape
        img[0:h, 0:w] = overLayList[totalFingers-1]


    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv.putText(img,f'{int(fps)}',(400,70),cv.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
    cv.imshow("Image",img)
    cv.waitKey(1)
