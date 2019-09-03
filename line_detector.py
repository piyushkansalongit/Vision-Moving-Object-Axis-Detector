import cv2
import numpy as np
from matplotlib import pyplot as plt
import os

def Hough(original_frame, filtered_frame, frame_save, thres):
    original_image = cv2.imread(original_frame)
    img = cv2.imread(filtered_frame)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray,20,150,apertureSize = 5)
    lines = cv2.HoughLinesP(edges,rho = 1,theta = np.pi/90,threshold = thres, minLineLength = 100, maxLineGap = 100)
    if thres==140:
        cv2.imwrite(frame_save, original_image)
        return
    if lines is None:
        cv2.imwrite(frame_save, original_image)
        return
    N = lines.shape[0]
    if(N > 4):
        return Hough(original_frame, filtered_frame, frame_save, thres+2)

    # try:
    #     xs = []
    #     initial_lines = []
    #     yb = 0
    #     slope = []
    #     count = 0
    #     for i in range(N):
    #         x1 = lines[i][0][0]
    #         y1 = lines[i][0][1]    
    #         x2 = lines[i][0][2]
    #         y2 = lines[i][0][3] 
    #         if(y1 > y2):
    #             temp = x1
    #             x1 = x2
    #             x2 = x1
    #             temp = y1
    #             y1 = y2
    #             y2 = temp
            
    #         temp = x1 - y1*((x2-x1)/(y2-y1))
    #         if(temp < 0.6 and temp > -0.6):
    #             continue
    #         yb += y2
    #         if(y2==y1):
    #             continue
    #         elif(x2==x1):
    #             xs.append(x1)
    #             slope.append(0)
    #         else:
    #             temp = x1 - y1*((x2-x1)/(y2-y1))
    #             if(temp > 0):
    #                 xs.append(temp)
    #             slope.append((y2-y1)/(x2-x1))
    #             count+=1
    #     xs.sort()
    #     slope.sort()
    #     yb = yb/N
    #     n = len(xs)
    #     xa = (xs[int(n/2)-1]+xs[int(n/2)]+xs[int(n/2)+1])/3
    #     slope = (slope[int(count/2)]+slope[int(count/2)+1])/2
    #     ya = 0
    #     if(slope==0):
    #         xb = xa
    #     else:
    #         xb = xa + (yb)/slope

    #     print("line:", xa, ya, xb, yb)
    #     cv2.line(original_image,(xa,ya),(xb,yb),(0,0,255),2)
    #     cv2.imwrite(frame_save, original_image)
    # except:
    #     cv2.imwrite(frame_save, original_image)

    try:
        print(original_frame, N, thres)
        xs = []
        initial_lines = []
        yb = 0
        slope = 0
        count = 0
        for i in range(N):
            x1 = lines[i][0][0]
            y1 = lines[i][0][1]    
            x2 = lines[i][0][2]
            y2 = lines[i][0][3] 
            if(y1 > y2):
                temp = x1
                x1 = x2
                x2 = x1
                temp = y1
                y1 = y2
                y2 = temp
            
            print(i, ":", x1, y1, x2, y2)
            if(y2>yb):
                yb = y2
            if(y2==y1):
                continue
            elif(x2==x1):
                xs.append(x1)
            else:
                xs.append(x1 - y1*((x2-x1)/(y2-y1)))
                slope += (y2-y1)/(x2-x1)
                count+=1
        xa = (min(xs)+max(xs))/2
        ya = 0
        if(slope==0):
            xb = xa
        else:
            xb = xa + (yb*count)/slope

        xa = int(xa)
        xb = int(xb)
        ya = int(ya)
        yb = int(yb)
        print("line:", xa, ya, xb, yb)
        cv2.line(original_image,(xa,ya),(xb,yb),(0,0,255),2)
        cv2.imwrite(frame_save, original_image)
    except:
        cv2.imwrite(frame_save, original_image)
        
if __name__ == '__main__':
    original_frames = "/media/piyush/D/sem5/COL780/Assignment1/1.frames/2"
    filtered_frames = "/media/piyush/D/sem5/COL780/Assignment1/3b.filtered/2"
    save_folder = "/media/piyush/D/sem5/COL780/Assignment1/4b.labelled/2"
    thres = 20
    for frame in os.listdir(original_frames):
        if(frame=="frame349.jpg"):
            frame_save = os.path.join(save_folder, frame)
            original_frame = os.path.join(original_frames, frame)
            filtered_frame = os.path.join(filtered_frames, frame)
            Hough(original_frame, filtered_frame, frame_save, thres)
                