from ultralytics import YOLO 
import cv2 

model = YOLO("yolov8n.pt")
cap = cv2.VideoCapture("RTPS_URL")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            if cls == 0:
                print("Person detected!")

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
