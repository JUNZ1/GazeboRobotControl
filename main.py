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

start= False
mask=5
while(True):


    # Capture frame-by-frame
    ret, frame = cap.read()
    # Our operations on the frame come here
    img = cv2.cvtColor(frame,0)

    cv2.imshow('image',img)
    '''
    try:
        cv2.imshow('crop',crop)
    except cv2.error:
            pass
    '''
    if start==True:
        roi=cv2.imread("Crop.jpg")
        roi = cv2.GaussianBlur(roi,(mask,mask),10)
        hsv_roi = cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)
        roi_v,roi_s,roi_h = cv2.split(hsv_roi)

        #threshold degerleri ilki min ikincisi max
        r_h_t=[roi_h.min(),roi_h.max()]
        r_s_t=[roi_s.min(),roi_s.max()]
        r_v_t=[roi_v.min(),roi_v.max()]


        img = cv2.GaussianBlur(img,(mask,mask),10)
        bos=img.copy()
        bos[:,:,:]=0
        hsv_img=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
        img_v,img_s,img_h = cv2.split(hsv_img)

        cv2.threshold(img_h,r_h_t[0],r_h_t[1],cv2.THRESH_BINARY+cv2.THRESH_OTSU,img_h)
        cv2.threshold(img_s,r_s_t[0],r_s_t[1],cv2.THRESH_BINARY+cv2.THRESH_OTSU,img_s)
        cv2.threshold(img_v,r_v_t[0],r_v_t[1],cv2.THRESH_BINARY+cv2.THRESH_OTSU,img_v)
        #son = np.hstack((img_v,img_s,img_h))

        kontur=img_s.copy()
        contours, hierarchy = cv2.findContours(kontur,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
        index=np.zeros(len(contours),int)

        for a in range(0,len(contours)):
            index[a]=len(contours[a])

        cnt = contours[index.argmax()]

        cv2.drawContours(bos, [cnt], 0, (0,255,0), 3)

        M = cv2.moments(cnt)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])

        (x,y),(MA,ma),angle = cv2.fitEllipse(cnt)

        #cv2.imshow("progress",img_s)

        if angle<150 and angle>120:
            print ("Saga Don")

        if angle<40 and angle>20:
            print ("Sola Don")

        if cy<120:
            print("ileri")

        if cy>340:
            print("geri")


        print("Merkez Noktalari",cx,"  ",cy,"  Aci====> ",angle)
        cv2.putText(bos,'ileri',(320,120), cv2.FONT_HERSHEY_SIMPLEX, 2,(255,0,0),1)
        cv2.putText(bos,'geri',(320,340), cv2.FONT_HERSHEY_SIMPLEX, 2,(255,0,0),1)
        cv2.circle(bos,(cx,cy), 20, (0,0,255), -1)
        cv2.imshow("Extracted Hand",bos)
    else:
        cv2.destroyWindow("progress")
        cv2.destroyWindow("Extracted Hand")

    k = cv2.waitKey(33)
    if k==1048689:    # 'q' tusu cikmak icin
        break
    elif k==-1:  # gerekiyor
        continue
    elif k==1048691:  # 's' tusu kaydediyor
        cv2.imwrite('Crop.jpg',crop)
        print 'goruntu kaydedildi'
    elif k==1048692:
        print("T tusuna basildi")
        start=not(start)
        print(start)