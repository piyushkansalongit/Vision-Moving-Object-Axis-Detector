import cv2
import os

def FrameCapture(video_path, frame_path):
    video = cv2.VideoCapture(video_path)
    count = 0
    success = 1
    while success:
        success, image = video.read()
        cv2.imwrite(os.path.join(frame_path, "frame%d.jpg"%count), image)
        count += 1

if __name__ == '__main__':
    video_folder = "/media/piyush/D/sem5/COL780/Assignment1/0. samples/"
    frame_folder = "/media/piyush/D/sem5/COL780/Assignment1/1. frames/"
    for video in os.listdir(video_folder):
        video_path = os.path.join(video_folder, video)
        
        frame_path = os.path.join(frame_folder, video[:-4])
        os.mkdir(frame_path)
        FrameCapture(video_path, frame_path)
