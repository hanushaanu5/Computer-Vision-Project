import cv2 as cv2
import numpy as np
import imutils 

counting_person=0
video = cv2.VideoCapture('CV_basket.mp4')

_, frame = video.read()
_, backup_frame = video.read()
print(frame.shape)
frame_count=0

while True:
    count_list=[]
    frame_count+=1
    
    difference = cv2.absdiff(frame, backup_frame)                                                                      # finding the absolute difference from image.
    grayscaling = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)                                      #converting image to grayscaling for better finding
    blur = cv2.GaussianBlur(grayscaling, (7,7), 1)                                                                        # blurring the image for smoother edging
    _, threshholding = cv2.threshold(blur, 40, 255, cv2.THRESH_BINARY)                             #making the contoru for outlining the moving character
    dilated = cv2.dilate(threshholding, None, iterations=4)                                                         #dialting the image for the better outcome
    contours_in_frame, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours_in_frame:
        (x, y, w, h) = cv2.boundingRect(contour)

        if cv2.contourArea(contour) < 900:
            continue
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        if w > 19 and h > 19:
            x_1=w/2
            y_1=h/2
            axis_x=x+x_1
            axis_y=y+y_1
            count_list.append([axis_x,axis_y])
            counting_person=len(count_list)
            print(len(count_list))
                
            
    image = imutils.resize(frame,400)
    cv2.putText(frame, "No of person in frame: {}                                   Frame passed: {} ".format(counting_person,frame_count)
                , (50, 50), cv2.FONT_HERSHEY_SIMPLEX,1
                , (1, 1, 254), 2)   
    cv2.imshow("feed", frame)
    frame = backup_frame
    _, backup_frame = video.read()

    if cv2.waitKey(50) == 27:
        break

cv2.destroyAllWindows()
video.release()
