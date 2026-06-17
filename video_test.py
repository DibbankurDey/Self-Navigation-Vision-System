import cv2
import os

video_path = "data/video/road_video.mp4"

print("Video Exists:", os.path.exists(video_path))

video = cv2.VideoCapture(video_path)

print("Video Opened:", video.isOpened())

while True:

    ret, frame = video.read()

    print("Frame Read:", ret)

    if not ret:
        break

    cv2.imshow("Video", frame)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()