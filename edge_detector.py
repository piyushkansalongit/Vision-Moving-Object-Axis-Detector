import cv2
import numpy as np
from matplotlib import pyplot as plt
import os
def Canny(initial_frame, filtered_frame, frame_save):
    print(initial_frame)
    image = cv2.imread(initial_frame)
    img = cv2.imread(filtered_frame)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray,20,150,apertureSize = 5)
    try:
        lines = cv2.HoughLinesP(edges,rho = 1,theta = np.pi/90,threshold = 70,minLineLength = 5, maxLineGap = 100)
        N = lines.shape[0]
        for i in range(N):
            x1 = lines[i][0][0]
            y1 = lines[i][0][1]    
            x2 = lines[i][0][2]
            y2 = lines[i][0][3] 
            slope = (y2-y1)/(x2-x1)
            print(x1, y1, x2, y2)
            if(slope < -2 or slope>2):
                cv2.line(image,(x1,y1),(x2,y2),(0,0,255),2)
        cv2.imwrite(frame_save, image)
    except:
        cv2.imwrite(frame_save, image)


if __name__ == '__main__':
    initial_frames = "/media/piyush/D/sem5/COL780/Assignment1/1.frames/2"
    filtered_frames = "/media/piyush/D/sem5/COL780/Assignment1/3b.filtered/2"
    save_folder = "/media/piyush/D/sem5/COL780/Assignment1/3c.edges/2"
    for frame in os.listdir(filtered_frames):
        if(frame=="frame100.jpg"):
            initial_frame = os.path.join(initial_frames, frame)
            frame_save = os.path.join(save_folder, frame)
            filtered_frame = os.path.join(filtered_frames, frame)
            Canny(initial_frame, filtered_frame, frame_save)
        
