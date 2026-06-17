from vision.lane_detection import detect_lanes
import cv2

result = detect_lanes("data/images/road.jpg")

if result is not None:

    cv2.namedWindow("Lane Detection", cv2.WINDOW_NORMAL)

    cv2.imshow("Lane Detection", result)

    cv2.waitKey(0)

    cv2.destroyAllWindows()