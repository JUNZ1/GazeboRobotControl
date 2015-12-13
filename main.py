from __future__ import division
import numpy as np
import cv2
from matplotlib import pyplot as plt
from time import *
global rakam
rakam=3

def nothing(x):
    global rakam
    rakam=x
    print "rakam===>",rakam
    pass

global rakam2
rakam2=3
def nothing2(x):
    global rakam2
    rakam2=x
    print "rakam2===>",rakam2
    pass


saban=cv2.imread('pardus.jpg')
saban = cv2.cvtColor(saban,0)
saban = cv2.resize(saban, (640, 480))

boxes = []
global crop
crop = cv2.resize(saban, (640, 480))

def on_mouse(event, x, y, flags, params):
    # global img


    if event == cv2.EVENT_LBUTTONDOWN:
         print 'Start Mouse Position: '+str(x)+', '+str(y)
         sbox = [x, y]
         boxes.append(sbox)
         # print count
         # print sbox

    elif event == cv2.EVENT_LBUTTONUP:
        print 'End Mouse Position: '+str(x)+', '+str(y)
        ebox = [x, y]
        boxes.append(ebox)
        print boxes
        try:
            global crop
            crop = img[boxes[-2][1]:boxes[-1][1],boxes[-2][0]:boxes[-1][0]]

        except cv2.error:
            return





cv2.namedWindow('image')
cv2.createTrackbar('sayi1', 'image',1,255,nothing)
cv2.createTrackbar('sayi2', 'image',1,255,nothing2)
cv2.setMouseCallback('image', on_mouse, 0)


cap = cv2.VideoCapture(1)


while(True):


    # Capture frame-by-frame
    ret, frame = cap.read()
    # Our operations on the frame come here
    img = cv2.cvtColor(frame,0)

    cv2.imshow('image',img)
    try:
        cv2.imshow('crop',crop)
    except cv2.error:
            pass


    k = cv2.waitKey(33)
    if k==1048689:    # 'q' tusu cikmak icin
        break
    elif k==-1:  # gerekiyor
        continue
    elif k==1048691:  # 's' tusu kaydediyor
        cv2.imwrite('Crop.jpg',crop)
        print 'goruntu kaydedildi'