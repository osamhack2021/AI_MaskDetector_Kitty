import cv2
import os

root_dir = os.path.dirname(os.path.abspath("README.md"))

model = (
    root_dir + "/resource/opencv_library/res10_300x300_ssd_iter_140000_fp16.caffemodel"
)
config = root_dir + "/resource/opencv_library/deploy.prototxt"


cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera open failed!")
    exit()

net = cv2.dnn.readNet(model, config)

if net.empty():
    print("Net open failed!")
    exit()

while True:
    ret, frame = cap.read()

    if ret:
        blob = cv2.dnn.blobFromImage(frame, 1, (300, 300), (104, 177, 123))
        net.setInput(blob)
        detect = net.forward()

        detect = detect[0, 0, :, :]
        (h, w) = frame.shape[:2]

        # print('--------------------------')
        for i in range(detect.shape[0]):
            confidence = detect[i, 2]
            if confidence < 0.5:
                break

            x1 = int(detect[i, 3] * w)
            y1 = int(detect[i, 4] * h)
            x2 = int(detect[i, 5] * w)
            y2 = int(detect[i, 6] * h)

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0))

            face = frame[y1:y2, x1:x2]
            width, height, channel = face.shape

            # print(x1, y1, x2, y2, width, height)
            # cv2.imshow("frame1", face)
            frame[0:width, 0:height] = face

            label = "Face: %4.3f" % confidence
            cv2.putText(
                frame,
                label,
                (x1, y1 - 1),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                1,
                cv2.LINE_AA,
            )

        cv2.imshow("frame", frame)

        if cv2.waitKey(1) == 27:
            break

    else:
        print("error")

cap.release()
cv2.destroyAllWindows()
