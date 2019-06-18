import cv2
import numpy as np

def nothing(x):
    pass


cv2.namedWindow("Trackbars")
cv2.createTrackbar("L-H", "Trackbars", 0,180, nothing)
cv2.createTrackbar("L-S", "Trackbars", 102, 255, nothing)
cv2.createTrackbar("L-V", "Trackbars", 200,255, nothing)
cv2.createTrackbar("H-H", "Trackbars", 25,180, nothing)
cv2.createTrackbar("H-S", "Trackbars", 241, 255, nothing)
cv2.createTrackbar("H-V", "Trackbars", 255,255, nothing)
cv2.createTrackbar("Kernal", "Trackbars", 2,10, nothing)

camera = cv2.VideoCapture(0)

kernel_dilation_erosion = np.ones((5,5), np.int8)

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

#    lower_range = np.array([L_H, L_S, L_V])
#    upper_range = np.array([H_H, H_S, H_V])
    lower_range = np.array([5,L_S,L_V])
    upper_range = np.array([15,255,255])
    kernel = np.ones((Kernal_varable, Kernal_varable), np.uint8)

    mask = cv2.inRange(hsv, lower_range, upper_range)
    mask = cv2.erode(mask, kernel)

    blur = cv2.GaussianBlur(mask, (5,5),2)

    opening = cv2.morphologyEx(blur, cv2.MORPH_OPEN, kernel_dilation_erosion)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel_dilation_erosion)

    #contour detecion

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt, True),True)
        cv2.drawContours(frame, [approx] ,0, (0,255,0), 5)
        if len(approx) > 10 and 20:
            print("ik zie een bal")

    cv2.imshow("Frame", frame)
    cv2.imshow("mask", closing)

    key = cv2.waitKey(60)
    if key == 27:
        break

camera.release()
cv2.destroyAllWindows()
