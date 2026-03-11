from ultralytics import YOLO
import cv2
import time
import os
import requests
import datetime
import csv

# ================= CONFIG =================
MODEL_PATH = "yolov8n.pt"
VIDEO_SOURCE = "test.mp4"
CONF_THRESHOLD = 0.6

GLOBAL_COOLDOWN = 20
ID_TIMEOUT = 10

TOKEN = "8543827401:AAHUeV3MTIApnJ4qkNQnOeLY-gbnqBUtH0U"
CHAT_ID = "8360061605"

# ===== Intruder Mode =====
INTRUDER_START = 17
INTRUDER_END = 6

# ===== ROI (Region Of Interest) =====
ROI_X1 = 100
ROI_Y1 = 100
ROI_X2 = 540
ROI_Y2 = 380

# ====================================

# ===== Folder setup =====
os.makedirs("screenshots", exist_ok=True)
os.makedirs("logs", exist_ok=True)

LOG_FILE = "logs/detection_log.csv"

if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp","track_id","confidence","event"])

# ====================================

def log_event(track_id, conf, event):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, track_id, conf, event])

# ====================================

def send_telegram_photo(photo_path, caption):
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"

    try:
        with open(photo_path, "rb") as photo:
            requests.post(
                url,
                data={
                    "chat_id": CHAT_ID,
                    "caption": caption
                },
                files={"photo": photo},
                timeout=5
            )
        print("Telegram sent")
    except Exception as e:
        print("Telegram error:", e)

# ====================================

def intruder_mode_active():
    hour = datetime.datetime.now().hour

    if INTRUDER_START > INTRUDER_END:
        return hour >= INTRUDER_START or hour < INTRUDER_END
    else:
        return INTRUDER_START <= hour < INTRUDER_END

# ====================================

model = YOLO(MODEL_PATH)
cap = cv2.VideoCapture(VIDEO_SOURCE)

print("Smart RT AI running...")
print("Press Q to exit")

last_global_alert = 0
active_ids = {}

# ===== Person Counting =====
unique_person_ids = set()

# ====================================

while True:

    ret, frame = cap.read()
    if not ret:
        break

    current_time = time.time()

    # ===== Draw ROI =====
    cv2.rectangle(frame,(ROI_X1,ROI_Y1),(ROI_X2,ROI_Y2),(255,0,0),2)

    # ===== Crop ROI for detection =====
    roi_frame = frame[ROI_Y1:ROI_Y2, ROI_X1:ROI_X2]

    results = model.track(roi_frame, persist=True, verbose=False)

    for r in results:

        for box in r.boxes:

            cls = int(box.cls[0])
            conf = float(box.conf[0])

            if cls == 0 and conf > CONF_THRESHOLD:

                track_id = int(box.id[0]) if box.id is not None else None
                if track_id is None:
                    continue

                # ===== Convert ROI coords to frame coords =====
                x1,y1,x2,y2 = map(int, box.xyxy[0])

                x1 += ROI_X1
                x2 += ROI_X1
                y1 += ROI_Y1
                y2 += ROI_Y1

                active_ids[track_id] = current_time

                # ===== Person Counting =====
                if track_id not in unique_person_ids:
                    unique_person_ids.add(track_id)
                    print("Total unique person:", len(unique_person_ids))

                # ===== Alert system =====
                if (current_time - last_global_alert) > GLOBAL_COOLDOWN:

                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    filename = f"screenshots/person_{track_id}_{int(current_time)}.jpg"

                    if intruder_mode_active():

                        cv2.imwrite(filename, frame)

                        caption = (
                            f"🚨 Smart RT AI Intruder\n"
                            f"Person ID: {track_id}\n"
                            f"Confidence: {conf:.2f}\n"
                            f"Time: {timestamp}"
                        )

                        send_telegram_photo(filename, caption)

                        log_event(track_id, conf, "intruder_alert")

                    else:

                        log_event(track_id, conf, "day_detection")

                    last_global_alert = current_time

                # ===== Draw detection =====
                cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)

                cv2.putText(
                    frame,
                    f"ID {track_id}",
                    (x1,y1-10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0,255,0),
                    2
                )

    # ===== Cleanup old IDs =====
    remove_ids = []

    for track_id,last_seen in active_ids.items():
        if current_time - last_seen > ID_TIMEOUT:
            remove_ids.append(track_id)

    for i in remove_ids:
        del active_ids[i]

    # ===== Show person count =====
    cv2.putText(
        frame,
        f"Total Person: {len(unique_person_ids)}",
        (20,40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0,255,255),
        2
    )

    cv2.imshow("Smart RT AI", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()