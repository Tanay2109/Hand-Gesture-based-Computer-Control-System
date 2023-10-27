import cv2
import cv2 as cv
import HandTrackingModule as htm
import numpy as np
import time
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wCam,hCam=640,640
cap=cv.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
pTime=0
detector=htm.handDetector(detectionCon=0.7,maxHands=1)

devices = AudioUtilities.GetSpeakers()  #boiler code for working with the audio of the device
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
volRange=volume.GetVolumeRange()

minVol=volRange[0]
maxVol=volRange[1]
vol=0
volBar=400
volPer = 0
area=0
while True:
    success,img=cap.read()
    #img=cv.flip(img,1)
    img=detector.findHands(img)
    lmList,bbox=detector.findPosition(img)
    if len(lmList)!=0:
      #print(lmList[4],lmList[8])
      area=(bbox[2]-bbox[0])*(bbox[3]-bbox[1])//100
      #print(area)
      if 150<area<1500: #Setting the area range for precise volume measurements
          #print("yes")
          length,img,lineInfo=detector.findDistance(4,8,img)
          #print(length,lineInfo)

          #print(length)
          if length<25: #To Mute
            cv.circle(img,(lineInfo[4],lineInfo[5]),10,(255,255,255),cv.FILLED)

             #HandRange 18-198
             #VolRange -65-0

          volBar=np.interp(length,[18,198],[400,150])
          volPer=np.interp(length,[18,198],[0,100])
          smoothness=10
          volPer=smoothness*round(volPer/smoothness) #For smoother volume changing
          fingers=detector.fingersUp()
          #print(fingers)
          if not fingers[4]: #to set the volume
              volume.SetMasterVolumeLevelScalar(volPer/100,None)
              cv.circle(img,(lineInfo[4],lineInfo[5]),10,(0,255,0),cv.FILLED)

    cv.rectangle(img,(50,150),(85,400),(0,255,0),3)
    cv.rectangle(img,(50,int(volBar)),(85,400),(255,255,255),cv2.FILLED) #For Volume Bar
    cv.putText(img,f'{int(volPer)}%',(40,450),cv.FONT_HERSHEY_COMPLEX,1,(255,255,255),2) #Volume Percent
    cVol=int(volume.GetMasterVolumeLevelScalar()*100)
    cv.putText(img,f"Volume Set: {int(cVol)}",(350,50),cv.FONT_HERSHEY_PLAIN,2,(255,0,0),3) # Displaying the Set Volume
    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv.putText(img,f"FPS: {int(fps)}",(40,70),cv.FONT_HERSHEY_PLAIN,2,(255,0,0),3)

    cv.imshow("Image",img)
    cv.waitKey(1)

