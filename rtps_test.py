import cv2

rtps_url = ""

cap = cv2.VideoCapture(rtps_url)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Gagal ambil frame")
        break

    cv2.imshow("CCTV", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()