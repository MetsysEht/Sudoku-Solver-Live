import cv2
import numpy as np
from Functions import *



if __name__ == '__main__':
    cap=cv2.VideoCapture(0)
    while True:
        success,img=cap.read()
        img=np.asarray(img)
        warp,pts1,pts2,flag=warped(img,0)
        if flag==True:
            thresh=extract(warp,0)
            arr,av=getmat(thresh)
            sol=solver(arr)
            #print (sol)
            bg,mask=output(warp,sol,av,arr)
            ans(bg,mask,pts1,pts2,img)

        cv2.imshow("Img",img)
        if cv2.waitKey(1) & 0xff==ord('q'):
            break