#############################################################
#Author: Arjun Sharma
#Email: <arjun_sharma123@outlook.com>
#############################################################
import cv2
import math
import time
import os
import sys
import pathlib

os.chdir(r"DATADIR/youtube/videos/")
framespath='DATADIR/youtube/frames/'

videos= os.listdir()
def FrameExtractor_one(vids, framespath, threadlabel):
    for k in vids:
        name = k[:-4]   
        videoFile = k
        imagesFolder = framespath + f'/{name}/'
        if len(os.listdir(imagesFolder))==0:
            start= time.time()
            cap = cv2.VideoCapture(videoFile)
            frameRate = cap.get(5) #frame rate
            while(cap.isOpened()):
                frameId = cap.get(1) #current frame number
                ret, frame = cap.read()
                if (ret != True):
                    break
                if (frameId % math.floor(frameRate) == 0):
                    filename = imagesFolder + "frame_" +  str(int(frameId)) + ".jpg"
                    cv2.imwrite(filename, frame)
            cap.release()
            print (threadlabel, " Done video! ", k, ' time taken: ', time.time()-start)
        else:
            print('video handled by threading script')

FrameExtractor_one(videos, framespath, 'yay')