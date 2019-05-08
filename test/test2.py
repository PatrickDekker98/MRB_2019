import cv2
import numpy as np

cap = cv2.VideoCapture(2)

val = 0;
lower_red = np.array([val,86,6])
upper_red = np.array([40 + val,250,250])
val2 = 30;
ratio = 3
kernel_size =3

def detectColour(frame, val):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lower_red, upper_red)
    
    res = cv2.bitwise_and(frame,frame,mask=mask)

    return res

def detectEdges(image, val):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    low_threshold = val
    img_blur = cv2.blur(gray, (3,3))
    detected_edges = cv2.Canny(image, low_threshold, low_threshold*ratio, kernel_size)
    mask = detected_edges != 0
    dst = image * (mask[:,:,None].astype(image.dtype))
    return dst

def detectCircle(circle, output):
    #frame = imutils.resize(frame, width=600)
    #blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    #hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(circle, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.2, 100)
    cv2.imshow('gray', gray)
    if circles is not None:
        circles = np.round(circles[0,:]).astype("int")

        for (x,y,r) in circles:
            cv2.circle(output, (x,y), r,(0,255,0),4)
            cv2.rectangle(output, (x - 5, y -5), (x+ 5, y + 5), (0,128,255), -1)





while(1):
    _, frame = cap.read()
    
    
    res = detectColour(frame, val)
    res2 = detectEdges(res, val2)
    detectCircle(frame, frame)


    cv2.imshow('frame',frame)
#    cv2.imshow('mask',mask)
    cv2.imshow('res',res)
    cv2.imshow('res2',res2)

    k = cv2.waitKey(1) & 0xFF 
    if k == ord('q'):
        break
    elif k == ord('k'):
        val += 1
        print("val: ", val)
    elif k == ord('l'):
        val -=1
        print("val: ", val)
    elif k == ord('o'):
        val2 += 1
    elif k == ord('p'):
        val2 -= 1

cv2.destroyAllWindows()

cap.release()
