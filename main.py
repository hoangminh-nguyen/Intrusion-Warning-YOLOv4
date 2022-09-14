import cv2
import numpy as np
from imutils.video import VideoStream
from yolodetect import YoloDetect

# input video from webcam
video = VideoStream(src=1).start()

# init yolo model
model = YoloDetect()

# function to draw the zone
points = []

def handle_left_click(event, x, y, flags, points):
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append([x, y])


def draw_polygon (frame, points):
    for point in points:
        frame = cv2.circle( frame, (point[0], point[1]), 5, (0,0,255), -1)

    frame = cv2.polylines(frame, [np.int32(points)], False, (255,0, 0), thickness=2)
    return frame

detect = False

while(1):
    # read frame in video
    frame = video.read()
    # flip the frame horizontally
    frame = cv2.flip(frame, 1)
    # Re create zone
    frame = draw_polygon(frame, points)

    # Detect human with YOLOv4 and draw bounding box
    if detect:
        frame = model.detect(frame= frame, points= points)

    # press 'q' to close the program
    key = cv2.waitKey(1)
    if key == ord("q"):
        break
    # press 'd' to confirm ending the zone
    elif key == ord('d'):
        points.append(points[0])
        detect = True
    
    # show frame on screen
    cv2.imshow("Intrusion Warning", frame)

    # left click to draw the zone
    cv2.setMouseCallback('Intrusion Warning', handle_left_click, points)

video.stop()
cv2.destroyAllWindows()
