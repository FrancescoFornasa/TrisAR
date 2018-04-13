import cv2
import numpy as np


def osserva_settore(roi):
    # TODO
    roi = cv2.cvtColor(roi, cv2.COLOR_RGB2GRAY)
    cerchi = cv2.HoughCircles(roi, cv2.HOUGH_GRADIENT, 1.1, 1)

    if cerchi is not None:
        cerchi = np.uint16(np.around(cerchi))
        cerchi = cerchi[0]

        # for c in cerchi

    return cerchi


def guarda_griglia(warped_frame, posizioni_angoli, dimensione_settore):

    board = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    while i < len(posizioni_angoli):
        angolo = posizioni_angoli[i]
        valore = osserva_settore(warped_frame[angolo[0]:angolo[0]+dimensione_settore[0], angolo[1]:angolo[1]+dimensione_settore[1]])
        if valore != ' ':
            board[i] = valore
        i = i+1

    return board







