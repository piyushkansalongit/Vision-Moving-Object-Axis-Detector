import os
import cv2
import numpy as np

def clean(img, save_path):
    kernel = np.ones((5,5),np.uint8)
    opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    # kernel = np.ones((3,3),np.uint8)
    closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    cv2.imwrite(save_path, closing)

if __name__ == '__main__':
    dirty_frames = "/media/piyush/D/sem5/COL780/Assignment1/2b.KNN/2"
    clean_frames = "/media/piyush/D/sem5/COL780/Assignment1/3b.filtered/2"

    for frame in os.listdir(dirty_frames):
        img = cv2.imread(os.path.join(dirty_frames, frame), 0)
        clean(img, os.path.join(clean_frames,frame))
