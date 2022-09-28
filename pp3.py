#from __future__ import print_function
from imutils.video import WebcamVideoStream,FPS
#from imutils.video import FPS
#import imutils
from imutils import resize
import cv2
import mediapipe as mp
from threading import Thread

class HandDet(Thread):
    def __init__(self):
        self.cap = WebcamVideoStream(src=0).start()
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(min_detection_confidence=0.5,min_tracking_confidence=0.5)
        self.mpDraw = mp.solutions.drawing_utils
        self.image = self.cap.read()
        self.x=0
        self.y=0
        self.state=True
        self.handOK= False

    def start(self):
        Thread(target = self.run, args=()).start()
        return self

    def run(self):
        handLms=None
        while self.state:
            self.image = self.cap.read()
            #self.image= cv2.flip(self.image,1)
            #DO PREPROCESSING SHIT
            #self.image= imutils.resize(self.image, width=600)
            self.image= resize(self.image, width=250)
            imageRGB = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            results = self.hands.process(imageRGB)
            if results.multi_hand_landmarks:
                self.handOK=True
                for handLms in results.multi_hand_landmarks: # working with each hand
                    for id, lm in enumerate(handLms.landmark):
                        
                        if id == 8:
                        #if id == 5:
                            h, w, c = self.image.shape
                            cx, cy = int(lm.x * w), int(lm.y * h)
                            cv2.circle(self.image, (cx, cy), 15, (205, 0, 255), cv2.FILLED)
                            self.x,self.y=cx,cy
                            #print("x="+str(cx))
                            #print("Y="+str(cy))
            else:
                self.handOK=False
            #print(self.handOK)
            self.mpDraw.draw_landmarks(self.image, handLms, self.mpHands.HAND_CONNECTIONS)
            cv2.imshow("Output", self.image)
            cv2.waitKey(1)
            if (cv2.waitKey(1) & 0xFF ==ord('q')):
                break



        cv2.destroyAllWindows()
        self.cap.stop()



    def stop(self):
        self.state=False
        cv2.destroyAllWindows()
        self.cap.stop()
