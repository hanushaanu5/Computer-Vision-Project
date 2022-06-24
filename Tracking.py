import cv2
import imutils
from collections import deque
import numpy as np
import time

start_frame = 0
stop_frame = 0

image_tracker_box=cv2.TrackerCSRT_create()

video_frame=cv2.VideoCapture('CV_basket.mp4')
ret,frames_image = video_frame.read()
cv2.putText(frames_image,'   select a player in black jersy for better result    ',  (10, 50), 
cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255),  1, cv2.LINE_4)
frames_image = imutils.resize(frames_image,height = 400, width = 1200)

cv2.imshow('Select and track',frames_image)

bb=cv2.selectROI('Select and track',frames_image)
image_tracker_box.init(frames_image,bb)

buffer_values = 60
pts = deque(maxlen=buffer_values)
i=1

fps=1

while True:
    _, frames_image = video_frame.read()
    
    stop_frame=time.time()
    fps=fps+1
    
    frames_image = imutils.resize(frames_image, height=400, width = 1200)
    
    (final,tracker_value)=image_tracker_box.update(frames_image)
    
    if final:
        
        (x,y,w,h)=[int(a) for a in tracker_value]
        
        cv2.rectangle(frames_image,(x,y),(x+w,y+h),(255,0,0),2)
        
        center = (x+w//2, y+h//2)
        radius = 2
        cv2.circle(frames_image, center, radius, (255, 255, 0), 2)
        pts.appendleft(center)
               
        cv2.putText(frames_image,'   Press- x -to exit the frame)                                             Fps={}'.format(fps),  (10, 50), 
        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255),  1, cv2.LINE_4)

    for i in np.arange(1, len(pts)):       
        if(pts[i-1] == None or pts[i] == None):
            continue
        
        thickness = int(np.sqrt(buffer_values / float(i + 1)) * 2.5)
        cv2.line(frames_image, pts[i-1], pts[i], (0, 0, 255), 4)
        
    cv2.imshow('Select and track',frames_image)
    
    key=cv2.waitKey(100) & 0xFF
    if key == ord('x'):
        break
video_frame.release()
cv2.destroyAllWindows()
