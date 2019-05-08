import numpy as np
import cv2

cap = cv2.VideoCapture(2)

ratio = 3
kernel_size = 3


detector=cv2.BRISK()

FLANN_INDEX_KDITREE=0
flannParam=dict(algorithm=FLANN_INDEX_KDITREE,tree=5)
flann=cv2.FlannBasedMatcher(flannParam,{})

trainImg=cv2.imread("cup.png",0)
trainKP,trainDesc=detector.detectAndCompute(trainImg,None)


def findCup(image, val):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    low_threshold = val
    img_blur = cv2.blur(gray, (3,3))
    detected_edges = cv2.Canny(image, low_threshold, low_threshold*ratio, kernel_size)
    mask = detected_edges != 0
    dst = image * (mask[:,:,None].astype(image.dtype))
    return dst
    
#    image = cv2.cvtColor(image, cv2.COLOR_BRG2RGB)

#    max_dimension= max(image.shape)

#    scale_dimension = max(image.shape)

#    scale = 700/max_dimension
#    image = cv2.resize(image, None, fx=scale, fy=scale)

#    image_blur = cv2.GaussianBlur(image, (7,7), 0)
#    image_blur_hsv = cv2.cvtColor(image_blur, cv2.COLOR_RGB2HSV)

#    min_red = np.array([0,100,80])
#    max_red = np.array([10,256,256])

#    mask1 = cv2.inRange(image_blur_hsv, min_red, max_red)

#    min_red2 = np.array([170, 100, 80])
#    max_red2 = np.array([180, 256, 256])

#    mask2 = cv2.inRange(image_blur_hsv, min_red2, max_red2)

#    mask = mask1+mask2

#    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15,15))
#    mask_closed



while(True):
    ret, frame = cap.read()

    QueryImg=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    queryKP,queryDesc=detectAndCompute(QueryImg,None)
    matches=flann.knnMatch(queryDesc, trainDesc, k=2)
    foodMatch=[]
    for m,n in matches:
        if(m.distance<0,75*n.distance):
            goodMatch.append(m)
    MIN_MATCH_COUNT = 30
    if(len(goodMatch)>=MIN_MATCH_COUNT):
        tp=[]
        qp=[]

        for m in goodMatch:
            tp.append(trainKP[m.trainIdx].pt)
            qp.append(queryKP[m.queryIdx].pt)

        tp,qp=np.float32((tp,qp))

        H,status=cv2.findHomography(tp,qp,cv2.RANSAC,3.0)

        h,w=trainImg.shape
        trainBorder=np.float32([[[0,0],[0,h-1],[w-1,h-1],[w-1,0]]])
        queryBorder=cv2.perspectiveTransform(trainBorder,H)
        cv2.polylines(QueryImgBGR,[np.int32(queryBorder)],True,(0,255,0),5)
    else:
        print("Not Enough match found- %d/%d"%(len(goodMatch),MIN_MATCH_COUNT))


    cv2.imshow('result',QueryImgBGR)
    
#    edges = findCup(frame, 30)

#    cv2.imshow('frame',frame)
#    cv2.imshow('edges',edges)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
