import os
from os.path import isfile, join
import cv2
import numpy as np
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--videoName', default="4.mp4", help='videoName')
    parser.add_argument('--videoPath', default="/media/piyush/D/sem5/COL780/Assignment1/0.samples", help='videoPath:')
    parser.add_argument('--savePath', default="/media/piyush/D/sem5/COL780/2017EE30539_2017CS10363/Output", help='savePath:')
    parser.add_argument('--subtractorHistory', default=200, help='history parameter for KNN subtractor.')
    parser.add_argument('--subtractorThreshold', default=100, help='threshold parameter for KNN subtractor.')
    parser.add_argument('--filterOpeningKernel', default=(5,5), help='kernel for opening operation')
    parser.add_argument('--filterClosingKernel', default=(5,5), help='kernel for closing operation')
    parser.add_argument('--thresholdHough', default=20, help='starting threshold for detecting Hough Lines')
    parser.add_argument('--fps', default=30, help='frames per second for the output video.')
    parser.add_argument('--stopTheshold', default=140, help='Threshold at which stop looking for hough lines.')
    parser.add_argument('--numLines', default=4, help='Number of Hough lines.')
    parser.add_argument('--rejectionSlope', default=0.6, help='Paramerter used to reject certain lines.')
    parser.add_argument('--minLineLength', default=5, help='Paramerter used to reject certain lines which are too small')
    parser.add_argument('--maxLineGap', default=100, help='Paramerter used in Hough.')
    args = parser.parse_args()
    return args

def Hough(args, originalFrame, filteredFrame, labelledFrame, threshold):
    original_image = cv2.imread(originalFrame)
    img = cv2.imread(filteredFrame)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray,20,150,apertureSize = 5)
    lines = cv2.HoughLinesP(edges,rho = 1,theta = np.pi/90,threshold = threshold, minLineLength = args.minLineLength, maxLineGap = args.maxLineGap)
    if threshold==args.stopTheshold:
        cv2.imwrite(labelledFrame, original_image)
        return
    if lines is None:
        cv2.imwrite(labelledFrame, original_image)
        return
    N = lines.shape[0]
    if(N > args.numLines):
        return Hough(args, originalFrame, filteredFrame, labelledFrame, threshold+2)

    try:
        xs = []
        initial_lines = []
        yb = 0
        slope = []
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
            
            temp = x1 - y1*((x2-x1)/(y2-y1))
            if(temp < args.rejectionSlope and temp > -1*(args.rejectionSlope)):
                continue
            yb += y2
            if(y2==y1):
                continue
            elif(x2==x1):
                xs.append(x1)
                slope.append(0)
            else:
                temp = x1 - y1*((x2-x1)/(y2-y1))
                if(temp > 0):
                    xs.append(temp)
                slope.append((y2-y1)/(x2-x1))
                count+=1
        xs.sort()
        slope.sort()
        yb = yb/N
        n = len(xs)
        xa = (xs[int(n/2)-1]+xs[int(n/2)]+xs[int(n/2)+1])/3
        slope = (slope[int(count/2)]+slope[int(count/2)+1])/2
        ya = 0
        if(slope==0):
            xb = xa
        else:
            xb = xa + (yb)/slope

        xa = int(xa)
        xb = int(xb)
        ya = int(ya)
        yb = int(yb)
        if(xa!=xb):
            slope = (yb-ya)/(xb-xa)
            if(slope < args.rejectionSlope and slope > -1*args.rejectionSlope):
                cv2.imwrite(labelledFrame, original_image)
                return
        cv2.line(original_image,(xa,ya),(xb,yb),(0,0,255),4)
        cv2.imwrite(labelledFrame, original_image)
    except:
        cv2.imwrite(labelledFrame, original_image)


def subtractor(args, videoFile, subtractedFrames):
    cap = cv2.VideoCapture(videoFile)
    fgbg = cv2.createBackgroundSubtractorKNN(history=args.subtractorHistory, dist2Threshold=args.subtractorThreshold, detectShadows=False)
    count = 0
    while(1):
        ret, frame = cap.read()
        fgmask = fgbg.apply(frame)

        if ret == True:
            ret, fgmask = cv2.threshold(fgmask, 0, 255, cv2.THRESH_OTSU)
            cv2.imwrite(os.path.join(subtractedFrames, "frame%d.jpg"%count), fgmask)
            count+=1
        else:
            break

def filtering(args, img, save_path):
    kernel = np.ones(args.filterOpeningKernel,np.uint8)
    img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    kernel = np.ones(args.filterClosingKernel,np.uint8)
    img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    cv2.imwrite(save_path, img)

def extractor(args, videoFile, frames):
    video = cv2.VideoCapture(videoFile)
    count = 0
    success = 1
    while success:
        success, image = video.read()
        cv2.imwrite(os.path.join(frames, "frame%d.jpg"%count), image)
        count += 1

def convert_frames_to_video(args,pathIn,pathOut,fps):
    frame_array = []
    files = [f for f in os.listdir(pathIn) if isfile(join(pathIn, f))]
 
    #for sorting the file names properly
    files.sort(key = lambda x: int(x[5:-4]))
 
    for i in range(len(files)):
        filename=os.path.join(pathIn,files[i])
        #reading each files
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        print(filename)
        #inserting the frames into an image array
        frame_array.append(img)
 
    out = cv2.VideoWriter(pathOut,cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
 
    for i in range(len(frame_array)):
        # writing to a image array
        out.write(frame_array[i])
    out.release()

def localizeObject(cwd, args):
    
    #Get the name of the video.
    videoName = args.videoName
    print("We will localize the moving rod in the %s video! Holdback and sit tight :)"%videoName)
    saveName = videoName[:-4]+".avi"
    #Get the path of the folder where videos are stored.
    videoPath = args.videoPath

    #Get the path of the folder where output needs to be stored.
    savePath = args.savePath

    #Path for the video file.
    videoFile = os.path.join(videoPath, videoName)

    #Path for saving the output file.
    saveFile = os.path.join(savePath, saveName)

    #Begin by background subtraction.
    #Making a folder to store the subtracted frames.
    print("We will first perform background subtraction")
    subtractedFrames = os.path.join(cwd, "subtractedFrames")
    os.mkdir(subtractedFrames)
    try:
        subtractor(args, videoFile, subtractedFrames)
    except:
        pass
    #Continuing with frame filtering.
    #Making a folder to store the filtered frames.
    print("Now let us move to the filtering of background subtracted frames")
    filteredFrames = os.path.join(cwd, "filteredFrames")
    os.mkdir(filteredFrames)
    for frame in os.listdir(subtractedFrames):
        img = cv2.imread(os.path.join(subtractedFrames, frame), 0)
        filtering(args, img, os.path.join(filteredFrames, frame))


    #Continuing with line and medial detection.
    #Breaking the video into frames.
    frames = os.path.join(cwd, "frames")
    labelled = os.path.join(cwd, "labelled")
    os.mkdir(frames)
    os.mkdir(labelled)
    try:
        print("Extracting the original frames")
        extractor(args, videoFile, frames)
    except:
        pass
    threshold = args.thresholdHough
    
    print("Detecting the medial axis")
    try:
        for frame in os.listdir(frames):
            labelledFrame = os.path.join(labelled, frame)
            originalFrame = os.path.join(frames, frame)
            filteredFrame = os.path.join(filteredFrames, frame)
            Hough(args, originalFrame, filteredFrame, labelledFrame, threshold)
    except:
        pass

    print("Stitching back in a video.")
    #Finally stitch all the labelled frames into a video.
    fps = args.fps
    convert_frames_to_video(args, labelled, saveFile, fps)
    
if __name__ == '__main__':
    args = parse_args()
    cwd = os.getcwd()
    localizeObject(cwd, args)
