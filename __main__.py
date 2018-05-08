from __future__ import print_function
import operator
import cv2
from ar_markers import detect_markers, HammingMarker
from cv2.cv2 import VideoCapture
import numpy as np
import tic_tac_toe_ai as ai
import visione

# Variabili gloabali
huPlayer = 'O'  # human
aiPlayer = 'X'  # ai
mouseX = -1
mouseY = -1


def posizione_mouse(event, x, y, flag, param):
    if event == cv2.EVENT_MOUSEMOVE:
        global mouseX
        mouseX = x
        global mouseY
        mouseY = y
    return


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
        i = i + 1

    if found == [True, True, True, True]:
        break

    cv2.imshow('CALIBRAZIONE', frame)
    cv2.setMouseCallback('CALIBRAZIONE', posizione_mouse)
    k = cv2.waitKey(1)
    if k == ord('q'):
        break
    if k == ord('r'):
        found = [False, False, False, False]
        markers = [HammingMarker(0), HammingMarker(0), HammingMarker(0), HammingMarker(0)]
        centers = [(0, 0), (0, 0), (0, 0), (0, 0)]

    if k == ord('1'):
        found[0] = True
        centers[0] = (mouseX, mouseY)
        contorno = np.array([(mouseX - 20, mouseY - 20), (mouseX + 20, mouseY - 20), (mouseX + 20, mouseY + 20),
                             (mouseX - 20, mouseY + 20)])
        markers[0] = HammingMarker(1, contorno)

    if k == ord('3'):
        found[1] = True
        centers[1] = (mouseX, mouseY)
        contorno = np.array([(mouseX - 20, mouseY - 20), (mouseX + 20, mouseY - 20), (mouseX + 20, mouseY + 20),
                             (mouseX - 20, mouseY + 20)])
        markers[1] = HammingMarker(3, contorno)

    if k == ord('5'):
        found[2] = True
        centers[2] = (mouseX, mouseY)
        contorno = np.array([(mouseX - 20, mouseY - 20), (mouseX + 20, mouseY - 20), (mouseX + 20, mouseY + 20),
                             (mouseX - 20, mouseY + 20)])
        markers[2] = HammingMarker(5, contorno)

    if k == ord('7'):
        found[3] = True
        centers[3] = (mouseX, mouseY)
        contorno = np.array([(mouseX - 20, mouseY - 20), (mouseX + 20, mouseY - 20), (mouseX + 20, mouseY + 20),
                             (mouseX - 20, mouseY + 20)])
        markers[3] = HammingMarker(7, contorno)

    frame_captured, frame = capture.read()

cv2.destroyAllWindows()

# TROVATI TUTTI I MARKER
for center in centers:
    cv2.circle(frame_orig, center, 1, (0, 0, 255), -1)

#cv2.imshow('FOUND!', frame_orig)
#cv2.waitKey()
#cv2.destroyAllWindows()

# COMPUTAZIONE OMOGRAFIA
border = (30, 30)
res_size = (640, 480)

dest = [(1 + border[0], 1 + border[1]), (res_size[0] + border[0], 1 + border[1]),
        (1 + border[0], res_size[1] + border[1]), (res_size[0] + border[0], res_size[1] + border[1])]

h, status = cv2.findHomography(np.asarray(centers), np.asarray(dest))

warped = cv2.warpPerspective(frame_orig, h, (res_size[0] + (2 * border[0]), res_size[1] + (2 * border[1])))

#cv2.imshow('WARP', warped)
#cv2.waitKey()
#cv2.destroyAllWindows()

# WARPING REALTIME e INIZIO GIOCO
board = [0, 1, 2, 3, 4, 5, 6, 7, 8]

dimensioni_settore = (int(res_size[0] / 4), int(res_size[1] / 4))
angoli_settori = [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)]

angoli_settori[0] = (border[0] + int(dimensioni_settore[0] / 2), border[1] + int(dimensioni_settore[1] / 2))
angoli_settori[1] = tuple(map(operator.add, angoli_settori[0], (int(dimensioni_settore[0]), 0)))
angoli_settori[2] = tuple(map(operator.add, angoli_settori[1], (int(dimensioni_settore[0]), 0)))
angoli_settori[3] = tuple(map(operator.add, angoli_settori[0], (0, int(dimensioni_settore[1]))))
angoli_settori[4] = tuple(map(operator.add, angoli_settori[3], (int(dimensioni_settore[0]), 0)))
angoli_settori[5] = tuple(map(operator.add, angoli_settori[4], (int(dimensioni_settore[0]), 0)))
angoli_settori[6] = tuple(map(operator.add, angoli_settori[3], (0, int(dimensioni_settore[1]))))
angoli_settori[7] = tuple(map(operator.add, angoli_settori[6], (int(dimensioni_settore[0]), 0)))
angoli_settori[8] = tuple(map(operator.add, angoli_settori[7], (int(dimensioni_settore[0]), 0)))

frame_captured, frame = capture.read()
while frame_captured:
    warped = cv2.warpPerspective(frame, h, (res_size[0] + (2 * border[0]), res_size[1] + (2 * border[1])))

    warped = visione.disegna(warped, board, angoli_settori, dimensioni_settore)
    cv2.imshow('GAME', warped)

    k = cv2.waitKey(1)

    if k == ord('q'):
        break
    if k == ord(' '):
        # PARSING DELL'IMMAGINE PER GUARDARE CONFIGURAZIONE BOARD
        nuova_board = visione.guarda_griglia(warped, board, angoli_settori, dimensioni_settore)
        if nuova_board == -1:
            continue

        board = nuova_board
        mossa = ai.trova_mossa_migliore(board, aiPlayer)
        board[mossa.index] = aiPlayer

    controllo_vittoria = ai.winning(board, huPlayer)
    if controllo_vittoria[0]:
        capture.release()
        cv2.destroyAllWindows()
        warped = visione.disegna(warped, board, angoli_settori, dimensioni_settore)
        warped = visione.disegna_fine(warped, huPlayer, controllo_vittoria[1], angoli_settori, dimensioni_settore)
        cv2.imshow("VITTORIA!", warped)
        cv2.waitKey()
        cv2.destroyAllWindows()
        break

    controllo_vittoria = ai.winning(board, aiPlayer)
    if controllo_vittoria[0]:
        capture.release()
        cv2.destroyAllWindows()
        warped = visione.disegna(warped, board, angoli_settori, dimensioni_settore)
        warped = visione.disegna_fine(warped, aiPlayer, controllo_vittoria[1], angoli_settori, dimensioni_settore)
        cv2.imshow("SCONFITTA!", warped)
        cv2.waitKey()
        cv2.destroyAllWindows()
        break

    if len(ai.empty_indexes(board)) == 0:
        capture.release()
        cv2.destroyAllWindows()
        warped = visione.disegna(warped, board, angoli_settori, dimensioni_settore)
        cv2.imshow("PAREGGIO!", warped)
        cv2.waitKey()
        cv2.destroyAllWindows()
        break

    frame_captured, frame = capture.read()
