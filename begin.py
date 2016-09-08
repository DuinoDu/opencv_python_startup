#!/usr/bin/env python

'''
It is a startup for opencv in python
====================

Usage
-----
startup.py [video file or folder containing videos]

Keys
----
ESC - exit
s   - slow
f   - fast
d   - stop
r   - restart
right arrow  - move foreward
'''


# Python 2/3 compatibility
from __future__ import print_function

import numpy as np
import cv2
import video
from common import anorm2, draw_str
from time import clock

def draw_detections(img, rects, thickness = 1):
    for x, y, w, h in rects:
        # the HOG detector returns slightly larger rectangles than the real objects.
        # so we slightly shrink the rectangles to get a nicer output.
        pad_w, pad_h = int(0.15*w), int(0.05*h)
        cv2.rectangle(img, (x+pad_w, y+pad_h), (x+w-pad_w, y+h-pad_h), (0, 255, 0), thickness)


def draw_hist(im):
    h = np.zeros((300,256,3))
    if len(im.shape)!=2:
        print("hist_lines applicable only for grayscale images")
        im = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    hist_item = cv2.calcHist([im],[0],None,[256],[0,256])
    cv2.normalize(hist_item,hist_item,0,255,cv2.NORM_MINMAX)
    hist=np.int32(np.around(hist_item))
    for x,y in enumerate(hist):
        cv2.line(h,(x,0),(x,y),(255,255,255))
    y = np.flipud(h)
    return y


class App:
    def __init__(self, video_src):
        self.video_src = video_src
        self.ch = 0
        self.cam = video.create_capture(self.video_src)
        
        # add other vars

    def run(self):
        # init local vars
        badframeCnt = 0
        delayTime = 20
        jump = 20

        while True:
            # read frame
            ret, frame = self.cam.read()
            if not ret:
                badframeCnt = badframeCnt + 1
                if badframeCnt > 3:
                    break
                else:
                    continue

            ######################
            # Add your code here #
            ######################












            # show result
            cv2.imshow("frame", frame)

            ####################
            # keyboard control #
            ####################
            self.ch = 0xFF & cv2.waitKey(delayTime) # 20
            ch = self.ch
            # Esc
            if ch == 27:
                break
            # faster
            if ch == ord('g'):
                delayTime = 1
            # fast
            if ch == ord('f'):
                delayTime = 20
            if ch == ord('1'):
                delayTime = 100
            if ch == ord('2'):
                delayTime = 300  
            if ch == ord('3'):
                delayTime = 600
            # slow
            if ch == ord('s'):
                delayTime = 1000
            # replay
            if ch == ord('r'):
                self.cam = video.create_capture(self.video_src)
            # stop   
            if ch == ord('d'):
                ch = 0xFF & cv2.waitKey(delayTime) 
                while ch != ord('d'):
                    ch = 0xFF & cv2.waitKey(delayTime)
                    continue;
            # move foreward > 
            if ch == 82:
                jump = jump + 20
                print("jupm speed: ", jump)
            if ch == 84:
                jump = (jump - 20 > 0) and (jump - 20) or jump
                print("jupm speed: ", jump)
            if ch == 83:
                for i in range(jump):
                    self.cam.read()


def getVideofiles(directory):
    import os
    if directory == 0:
        return [str(0)]
    if not os.path.exists(directory):
        print("file or directory not exists")
    else:
        if os.path.isfile(directory):
            return [directory]
        elif os.path.isdir(directory):
            files = os.listdir(directory)
            videos = []
            for f in files:
                if f.find("mp4") > 0 and f.find("src") < 0:
                    videos.append(directory+"/"+f)
            return videos


def main():
    import sys
    try:
        video_src = sys.argv[1]
    except:
        video_src = 0

    print(__doc__)
    
    videos = getVideofiles(video_src)

    for video in videos:
        print("current video:"+video)
        app = App(video)
        app.run()
        if app.ch == 27:
            break
    
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
