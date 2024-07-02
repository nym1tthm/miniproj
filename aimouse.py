import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy
import pyautogui as pg

widCam,heiCam=620,450
frameR = 120
smooth=15
plocx,plocy=0,0
clocx,clocy=0,0

cap = cv2.VideoCapture(0)
cap.set(3,600)
cap.set(4,450)
pTime = 0

detector = htm.handDetector(maxHands=1)
scrWid ,scrHei = autopy.screen.size()
#print(scrWid ,scrHei)

while True:
    sucess, img = cap.read()
    detector.findHands(img)
    lmList = detector.findPosition(img)
    
    if len(lmList) !=0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        fingers = detector.fingersUp()        

        if fingers[1] ==1 and fingers[2]==0:
            x3 = np.interp(x1,(frameR, widCam-frameR), (0, scrWid))
            y3 = np.interp(y1,(frameR, heiCam-frameR), (0, scrHei))

            clocx = plocx + (x3 - plocx)/smooth
            clocy = plocy + (y3 - plocy)/smooth

            autopy.mouse.move(scrWid-clocx,clocy)
            
            cv2.circle(img,(x1,y1),15,(0,0,180),cv2.FILLED)
            plocx,plocy = clocx,clocy
            if fingers[4] == 1:
                 pg.mouseDown()
                  
                      
            
        if fingers[1] == 1 and fingers[2] == 1:
            length ,img,lineinfo = detector.findDistance(8,12,img)
            #print(length)
            if length < 25:
                    
                    autopy.mouse.click()
                    cv2.circle(img,(lineinfo[4],lineinfo[5]),15,(255,255,0))
        
        
        
        if fingers[0] == 1 and fingers[1] == 0:
            pg.scroll(-20)
        if all(fingers[i] == 0 for i in range(0,4)) and fingers[4] == 1 :
            pg.scroll(20)
        if fingers[1] == 0 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1: 
                 pg.hotkey('winleft','down')
                 time.sleep(2)
        if all(fingers) == True:
            pg.hotkey('ctrl','c')
        if fingers[0] == 0 and fingers[4] == 0 and all(fingers[i] == 1 for i in range(1,4)):     
            pg.click(button='right')
        
        


    cTime=time.time()
    fps = 1/(cTime-pTime)
    pTime=cTime
    # Display FPS in the bottom right corner of the image
    cv2.putText(img, str(int(fps)), (img.shape[1] - 100, img.shape[0] - 20),
            cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 2)


    cv2.imshow("aimouse",img)
    cv2.waitKey(1)
