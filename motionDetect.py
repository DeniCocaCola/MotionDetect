# OpenCV Motion Detection
# @DeniCocaCola
#
# WIP: Writing movement timestamps to Times.csv file
# WIP: Error handling


import cv2, time, pandas
from datetime import datetime


first_frame = None
status_list = [None,None]
times = []
df=pandas.DataFrame(columns=["Start","End"])

print("TIP: Click the 'x' KEY to close all video windows")
print("Detect from camera? <Y/N>: ")
useCam = input()

if useCam in {"Y","y"}:
    videoSrc = 0
elif useCam in {"N","n"}:
    videoSrc = input("Enter video file path: ")
else:
    print("Error")
    exit

video = cv2.VideoCapture(videoSrc) #"C:\\Users\\West\\Videos\\shock.mp4"

while True:
    check, frame = video.read()
    print (frame)
    status = 0
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #Converts each frame into gray scale
    gray = cv2.GaussianBlur(gray,(21,21),0) #Converts gray scale frame to GaussianBlur
    cv2.imshow("Capturing", gray)
    key = cv2.waitKey(1) #Generates new frame after 1ms
    if first_frame is None:
        first_frame=gray
        continue
    delta_frame = cv2.absdiff(first_frame,gray) #Calculates the difference between the first frame and other frames
    thresh_delta = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1] #Threshold value, will convert the difference with less than 30 to black. Greater will convert to white
    thresh_delta = cv2.dilate(thresh_delta, None, iterations=0) # ^^^^
    (cnts, hierarchy) = cv2.findContours(thresh_delta.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)# Adds the borders

    for contour in cnts:
        if cv2.contourArea(contour) < 1000:  #Basically sensitivity. Removes noise/shadows
            continue
        status=1
        (x,y,w,h) = cv2.boundingRect(contour)               #\/ \/
        cv2.rectangle(frame, (x,y), (x+w,y+h),(0,255,0), 3) #Creates box around object in frame

    status_list.append(status)
    status_list=status_list[-2:]
    if status_list[-1]==1 and status_list[-2]==0:
        times.append(datetime.now())
    if status_list[-1]==0 and status_list[-2]==1:
        times.append(datetime.now())
    
    cv2.imshow("frame", frame)
    cv2.imshow("Capturing", gray)
    cv2.imshow("delta", delta_frame)
    cv2.imshow("thresh", thresh_delta)

    if key == ord("x"): # 'x' will close the active window
        break


print(status_list)
print(times)

for i in range(0, len(times),2):
    df=df.append({"Start":times[i],"End":times[i+1]}, ignore_index=True)

'''
df.to_csv("Times.csv") #Currently creates the file, but no timestamps?
  '''      

video.release()
cv2.destroyAllWindows()
