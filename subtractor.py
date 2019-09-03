import numpy as np
import cv2
import os

def subtractor(video_path, frame_path):
    cap = cv2.VideoCapture(video_path)
    fgbg = cv2.createBackgroundSubtractorKNN(history=200, dist2Threshold=100, detectShadows=False)
    count = 0
    while(1):
        ret, frame = cap.read()
        fgmask = fgbg.apply(frame)

        if ret == True:
            ret, fgmask = cv2.threshold(fgmask, 0, 255, cv2.THRESH_OTSU)
            cv2.imshow('frame',fgmask)
            cv2.imwrite(os.path.join(frame_path, "frame%d.jpg"%count), fgmask)
            count+=1
            if cv2.waitKey(30) & 0xFF == ord('q'):
                break
        else:
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    video_path = "/media/piyush/D/sem5/COL780/Assignment1/0.samples/2.mp4"
    frame_path = "/media/piyush/D/sem5/COL780/Assignment1/2b.KNN/2"
    # for video in os.listdir(video_folder):
    #     video_path = os.path.join(video_folder, video)
        
    #     frame_path = os.path.join(frame_folder, video[:-4])
    #     os.mkdir(frame_path)
    subtractor(video_path, frame_path)