import cv2
import numpy as np
from PID import PID
from arduino_test import send_fan
import serial

def nothing(x):
    pass


cv2.namedWindow("Trackbars")
cv2.createTrackbar("L-H", "Trackbars", 10,180, nothing)
cv2.createTrackbar("L-S", "Trackbars", 102, 255, nothing)
cv2.createTrackbar("L-V", "Trackbars", 200,255, nothing)
cv2.createTrackbar("H-H", "Trackbars", 25,180, nothing)
cv2.createTrackbar("H-S", "Trackbars", 241, 255, nothing)
cv2.createTrackbar("H-V", "Trackbars", 255,255, nothing)
cv2.createTrackbar("Kernal", "Trackbars", 2,10, nothing)

camera = cv2.VideoCapture(0)

kernel_dilation_erosion = np.ones((5,5), np.int8)

ball_height = 0
ball_aim = 0
PID_controller = PID(10,0,0)

arduino = serial.Serial("/dev/ttyUSB0", 115200)

while True:
    _, frame = camera.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    L_H = cv2.getTrackbarPos("L-H","Trackbars")
    L_S = cv2.getTrackbarPos("L-S", "Trackbars")
    L_V = cv2.getTrackbarPos("L-V", "Trackbars")
    H_H = cv2.getTrackbarPos("H-H","Trackbars")
    H_S = cv2.getTrackbarPos("H-S", "Trackbars")
    H_V = cv2.getTrackbarPos("H-V", "Trackbars")

    Kernal_varable= cv2.getTrackbarPos("Kernal", "Trackbars")

    lower_range = np.array([L_H, L_S, L_V])
    upper_range = np.array([H_H, H_S, H_V])
    lower_range1 = np.array([175, 100, 20])
    upper_range1 = np.array([255,255,255])
    kernel = np.ones((Kernal_varable, Kernal_varable), np.uint8)

    mask_object_two = cv2.inRange(hsv, lower_range1, upper_range1)
    mask = cv2.inRange(hsv, lower_range, upper_range)
    mask = cv2.erode(mask, kernel)


    closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel_dilation_erosion)
    opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel_dilation_erosion)

    closing_object_two = cv2.morphologyEx(mask_object_two, cv2.MORPH_CLOSE, kernel_dilation_erosion)
    opening_object_two = cv2.morphologyEx(closing_object_two, cv2.MORPH_OPEN, kernel_dilation_erosion)

    circles = cv2.HoughCircles(opening, cv2.HOUGH_GRADIENT,2,20 ,param1=11,param2=11,minRadius=0,maxRadius=0)
    if circles is not None:
        circles = np.uint16(np.around(circles))
        i = circles[0][0]
        if (i[1] != 0 or i[1] != frame.shape[0]):
            ball_height = i[1]
            cv2.circle(frame, (i[0], i[1]), i[2], (0,255,0), 2)
            #cv2.circle(frame, (i[0], i[1]), 2, (0, 0, 255), 3)
            cv2.line(frame, (0, i[1]), (frame.shape[1], i[1]),(0,255,0), 3)
        
    #contour detecion

    contours, _ = cv2.findContours(opening_object_two, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #cv2.drawContours(frame, contours, -1, (255, 0, 0), 3)

    for cnt in contours:
        approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt, True),True)
        #cv2.drawContours(frame, [approx] ,0, (255,0,0), 5)
        #if len(approx) > 2 and len(approx) < 10:
        if len(approx) >4:
            #cv2.drawContours(frame, [approx] ,0, (255,0,0), 5)
            x,y,w,h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
            center = y + h/2
            ball_aim = center
            cv2.line(frame, (0, int(center)), (frame.shape[1], int(center)),(0,0,255), 3)
            break

    cv2.imshow("Frame", frame)
    #cv2.imshow("mask", closing)
    cv2.imshow("mask_object_two", opening_object_two)
    error = ball_height - ball_aim + frame.shape[0]
    val = PID_controller.Calc(error)
    val = int(((val / frame.shape[0]) / 10) *255)
    if val > 255:
        val = 255
    print(val)
    send_fan( val, arduino)

    key = cv2.waitKey(60)
    if key == 27:
        break

camera.release()
cv2.destroyAllWindows()
