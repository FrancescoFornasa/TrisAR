from __future__ import print_function
import cv2
from ar_markers import detect_markers, HammingMarker
from cv2.cv2 import VideoCapture
import numpy as np

# INIZIALIZZAZIONE CAMERA
print('Press "q" to quit')
capture = cv2.VideoCapture(1)  # type: VideoCapture

capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1280)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 720)

if capture.isOpened():  # try to get the first frame
    frame_captured, frame = capture.read()
else:
    frame_captured = False

# CALIBRAZIONE TRAMITE MARKERS AR
timer = 0
while frame_captured:
    frame_orig = frame.copy()  # type: object
    markers = detect_markers(frame)
    found = [False, False, False, False]

    for marker in markers:  # type: HammingMarker
        marker.highlite_marker(frame)
        if marker.id == 1:
            found[0] = True
        if marker.id == 3:
            found[1] = True
        if marker.id == 5:
            found[2] = True
        if marker.id == 7:
            found[3] = True

    if found == [True, True, True, True]:
        timer = timer + 1
    else:
        timer = 0

    if timer == 1:
        break

    cv2.imshow('Test Frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    frame_captured, frame = capture.read()


# capture.release()
cv2.destroyAllWindows()

# TROVATI TUTTI I MARKER
centers = [(0, 0), (0, 0), (0, 0), (0, 0)]
for marker in markers:
    if marker.id == 1:
        centers[0] = marker.center
    if marker.id == 3:
        centers[1] = marker.center
    if marker.id == 5:
        centers[2] = marker.center
    if marker.id == 7:
        centers[3] = marker.center

for center in centers:
    cv2.circle(frame_orig, center, 1, (0, 0, 255), -1)

cv2.imshow('FOUND!', frame_orig)
cv2.waitKey()
# When everything done, release the capture
cv2.destroyAllWindows()

# COMPUTAZIONE OMOGRAFIA
border = (30, 30)
res_size = (640, 480)
dest = [(1+border[0], 1+border[1]), (res_size[0]+border[0], 1+border[1]), (1+border[0], res_size[1]+border[1]), (res_size[0]+border[0], res_size[1]+border[1])]
print(dest, "\n")

h, status = cv2.findHomography(np.asarray(centers), np.asarray(dest))

warped = cv2.warpPerspective(frame_orig, h, (res_size[0]+(2*border[0]), res_size[1]+(2*border[1])))

cv2.imshow('WARP', warped)
cv2.waitKey()
cv2.destroyAllWindows()

# WARPING REALTIME
frame_captured, frame = capture.read()
print(capture.isOpened())
while frame_captured:
    warped = cv2.warpPerspective(frame, h, (res_size[0] + (2 * border[0]), res_size[1] + (2 * border[1])))
    cv2.imshow('g', warped)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    frame_captured, frame = capture.read()

capture.release()
cv2.destroyAllWindows()
