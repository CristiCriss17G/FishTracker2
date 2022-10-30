import cv2
# helping tracker class
from tracker import *

# Create tracker object
tracker = EuclideanDistTracker()

# Read video
video_path = "sample/fish.mp4"

cap = cv2.VideoCapture(video_path)

# Object detection from camera
object_detector = cv2.createBackgroundSubtractorKNN(
    history=100, dist2Threshold=500.0)


while cap.isOpened():
    ret, frame = cap.read()
    # height, width, _ = frame.shape

    # Extract Region of interest
    roi = frame[5: 715, 50: 1200]

    # 1. Object Detection
    mask = object_detector.apply(roi)
    _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
    
    contours, _ = cv2.findContours(
        mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    detections = []
    for cnt in contours:
        # Calculate area and remove small elements
        area = cv2.contourArea(cnt)
        if area > 400:
            x, y, w, h = cv2.boundingRect(cnt)

            detections.append([x, y, w, h])

    # 2. Object Tracking
    boxes_ids = tracker.update(detections)
    for box_id in boxes_ids:
        x, y, w, h, id = box_id
        cv2.putText(roi, str(id), (x, y - 15),
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 3)

    # cv2.imshow("roi", roi)
    cv2.imshow("Mask", mask)
    cv2.imshow("Frame", frame)

    key = cv2.waitKey(30)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
