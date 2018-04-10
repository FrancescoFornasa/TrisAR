from __future__ import print_function
import cv2
from ar_markers import detect_markers, HammingMarker
from cv2.cv2 import VideoCapture

print('Press "q" to quit')
capture = cv2.VideoCapture(1)  # type: VideoCapture

capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1280)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 720)

if capture.isOpened():  # try to get the first frame
    frame_captured, frame = capture.read()
else:
    frame_captured = False

timer = 0
while frame_captured:
    frame_orig = frame.copy()  # type: object
    markers = detect_markers(frame)
    found = [False, False, False]

    for marker in markers:  # type: HammingMarker
        marker.highlite_marker(frame)
        if marker.id == 1:
            found[0] = True
        if marker.id == 3:
            found[1] = True
        if marker.id == 7:
            found[2] = True

    if found == [True, True, True]:
        timer = timer + 1
    else:
        timer = 0

    if timer == 2:
        break

    cv2.imshow('Test Frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    frame_captured, frame = capture.read()

centers = [(0, 0), (0, 0), (0, 0)]
for marker in markers:
    if marker.id == 1:
        centers[0] = marker.center
    if marker.id == 3:
        centers[1] = marker.center
    if marker.id == 7:
        centers[2] = marker.center

for center in centers:
    cv2.circle(frame_orig, center, 5, (0, 0, 255), -1)
    print(center, "\n")

cv2.imshow('FOUND!', frame_orig)
cv2.waitKey()
# When everything done, release the capture
capture.release()
cv2.destroyAllWindows()
