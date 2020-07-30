import numpy as np 
import cv2 
import imutils 
import datetime 
  
   
gun_cascade = cv2.CascadeClassifier('gun.xml') 
camera = cv2.VideoCapture(0)
firstFrame = None
gun_exist = False
gun_last_detected = 99999999999999 

Lastx = 0
Lasty = 0
Lastw = 0
Lasth = 0

def placeRec(frame, x, y, w, h, color):

    print(
        "Lastx = " + str(Lastx),
        "Lasty = " +  str(Lasty),
        "Lastw = " +  str(Lastw),
        "Lasth = " +  str(Lasth))
    frame = cv2.rectangle(frame, 
        (x, y), 
        (x + w, y + h), 
        color, 2)

while True: 
      
    ret, frame = camera.read()
    
    frame = imutils.resize(frame, width = 500) 
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
    graydisplayed = gray   
    gun = gun_cascade.detectMultiScale(gray, 
                                       1.3, 5, 
                                       minSize = (100, 100)) 
       
    if len(gun) > 0: 
        gun_exist = True
        gun_last_detected = 0
           
    for (x, y, w, h) in gun: 
        Lastx = x
        Lasty = y
        Lastw = w
        Lasth = h
        placeRec(frame, x, y, w, h, (255, 0, 0))
        placeRec(graydisplayed, x, y, w, h, (255, 0, 0))

        roi_gray = gray[y:y + h, x:x + w] 
        roi_color = frame[y:y + h, x:x + w]     
    
    if firstFrame is None: 
        firstFrame = gray 
        continue
    
    if gun_last_detected != 0 and gun_last_detected < 200:
        placeRec(frame, Lastx, Lasty, Lastw, Lasth, (0, 255, 0))
        placeRec(graydisplayed, Lastx, Lasty, Lastw, Lasth, (0, 255, 0))

    # print(datetime.date(2019)) 
    # draw the text and timestamp on the frame 
    cv2.putText(frame, datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), 
                (10, frame.shape[0] - 10), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                0.35, (0, 0, 255), 1) 
   
    cv2.putText(graydisplayed, datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), 
                (10, frame.shape[0] - 10), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                0.35, (0, 0, 255), 1) 
    
    cv2.imshow("Security Feed", frame)
    key = cv2.waitKey(1) & 0xFF
      
    if key == ord('q'): 
        break
  
    if gun_exist: 
        print("guns detected " + datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
        gun_last_detected = 0
    else:
        gun_last_detected += 1
    gun_exist = False
    
else: 
    print("guns NOT detected") 
  
camera.release() 
cv2.destroyAllWindows() 