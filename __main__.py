from __future__ import print_function
import cv2
from ar_markers import detect_markers, HammingMarker
from cv2.cv2 import VideoCapture
import numpy as np
import tic_tac_toe_ai as ai
import visione

# Variabili gloabali
huPlayer = 'O'  # human
aiPlayer = 'X'  # ai

# INIZIALIZZAZIONE CAMERA
print('Press "q" to quit or "r" to reset the calibration')

capture = cv2.VideoCapture(1)  # type: VideoCapture

# capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1366)
# capture.set(cv2.CAP_PROP_FRAME_WIDTH, 768)

if capture.isOpened():  # try to get the first frame
    frame_captured, frame = capture.read()
else:
    frame_captured = False

# CALIBRAZIONE TRAMITE MARKERS AR
timer = 0
found = [False, False, False, False]
markers = [HammingMarker(0), HammingMarker(0), HammingMarker(0), HammingMarker(0)]
centers = [(0, 0), (0, 0), (0, 0), (0, 0)]

while frame_captured:
    frame_orig = frame.copy()  # type: object
    actual_markers = detect_markers(frame)

    for marker in actual_markers:  # type: HammingMarker
        if marker.id == 1:
            markers[0] = marker
            found[0] = True
            centers[0] = marker.center
        if marker.id == 3:
            markers[1] = marker
            found[1] = True
            centers[1] = marker.center
        if marker.id == 5:
            markers[2] = marker
            found[2] = True
            centers[2] = marker.center
        if marker.id == 7:
            markers[3] = marker
            found[3] = True
            centers[3] = marker.center

    i = 0
    while i < len(markers):
        if found[i]:
            markers[i].highlite_marker(frame)
        i = i+1

    if found == [True, True, True, True]:
        break

    cv2.imshow('CALIBRAZIONE', frame)
    k = cv2.waitKey(1)
    if k == ord('q'):
        break
    if k == ord('r'):
        found = [False, False, False, False]
        markers = [HammingMarker(0), HammingMarker(0), HammingMarker(0), HammingMarker(0)]
        centers = [(0, 0), (0, 0), (0, 0), (0, 0)]

    frame_captured, frame = capture.read()


cv2.destroyAllWindows()

# TROVATI TUTTI I MARKER
for center in centers:
    cv2.circle(frame_orig, center, 1, (0, 0, 255), -1)

cv2.imshow('FOUND!', frame_orig)
cv2.waitKey()
cv2.destroyAllWindows()

# COMPUTAZIONE OMOGRAFIA
border = (30, 30)
res_size = (640, 480)

angoli_settori = []  # TODO CALCOLARLI
dimensioni_settore = (0, 0)  # TODO CALCOLARLI

dest = [(1+border[0], 1+border[1]), (res_size[0]+border[0], 1+border[1]), (1+border[0], res_size[1]+border[1]), (res_size[0]+border[0], res_size[1]+border[1])]

h, status = cv2.findHomography(np.asarray(centers), np.asarray(dest))

warped = cv2.warpPerspective(frame_orig, h, (res_size[0]+(2*border[0]), res_size[1]+(2*border[1])))

cv2.imshow('WARP', warped)
cv2.waitKey()
cv2.destroyAllWindows()

# WARPING REALTIME e INIZIO GIOCO
board = [0, 1, 2, 3, 4, 5, 6, 7, 8]

frame_captured, frame = capture.read()
while frame_captured:
    warped = cv2.warpPerspective(frame, h, (res_size[0] + (2 * border[0]), res_size[1] + (2 * border[1])))
    cv2.imshow('g', warped)

    # TODO DISEGNA REALTA AUMENTATA

    k = cv2.waitKey(1)

    if k == ord('q'):
        break
    if k == ord(' '):
        # PARSING DELL'IMMAGINE PER GUARDARE CONFIGURAZIONE BOARD
        board = visione.guarda_griglia(warped, angoli_settori, dimensioni_settore)
        print("\nmossa\n")

    if ai.winning(board, huPlayer):
        print("\nHAI VINTO!\n")
        break

    #mossa = ai.trova_mossa_migliore(board, aiPlayer)
    #board[mossa] = aiPlayer

    if ai.winning(board, aiPlayer):
        print("\nHAI PERSO!\n")
        break

    if len(ai.empty_indexes(board)) == 0:
        print("\nPAREGGIO!\n")
        break

    frame_captured, frame = capture.read()


capture.release()
cv2.destroyAllWindows()
