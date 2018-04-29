import cv2
import numpy as np
import tic_tac_toe_ai as ai
import operator
import imutils
import time

soglia = 2  # soglia alta fa piu falsi positivi
disegno_cerchio = cv2.imread('./rainbow.png', cv2.IMREAD_UNCHANGED)


def osserva_settore(roi):
    roi = cv2.cvtColor(roi, cv2.COLOR_RGB2GRAY)

    cerchi = cv2.HoughCircles(roi, cv2.HOUGH_GRADIENT, soglia, 0.5)

    if cerchi is not None:
        cerchi = np.uint16(np.around(cerchi))
        cerchi = cerchi[0]

        for c in cerchi:
            roi = cv2.circle(roi, (c[0], c[1]), c[2], (255, 0, 255))

    return cerchi is not None


def guarda_griglia(warped_frame, board, posizioni_angoli, dimensione_settore):
    indici = ai.empty_indexes(board)
    trovata_mossa = False

    for i in indici:
        angolo = posizioni_angoli[i]
        valore = osserva_settore(
            warped_frame[angolo[1]:angolo[1] + dimensione_settore[1], angolo[0]:angolo[0] + dimensione_settore[0]])

        if valore:  # CERCHIO
            if trovata_mossa:
                print("\nNon Si Bara! Hai fatto troppe mosse in un solo turno!\nNe tengo solo una!")
            else:
                board[i] = 'O'
                trovata_mossa = True

    if not trovata_mossa:
        print ("\nNon hai fatto nessuna mossa?\nRiprova premendo barra spaziatrice dopo aver fatto la tua mossa!\n")
        return -1

    return board


def disegna_settore(immagine, pezzo, angolo_settore, dimensione_settore):
    if pezzo == 'X':
        immagine = cv2.drawMarker(immagine,
                                  (angolo_settore[0] + int(dimensione_settore[0] / 2),
                                   angolo_settore[1] + int(dimensione_settore[1] / 2)),
                                  (0, 0, 255), cv2.MARKER_TILTED_CROSS, int(dimensione_settore[0] / 2), 3)
    elif pezzo == 'O':
        cerchio = disegno_cerchio.copy()
        cerchio = imutils.rotate(cerchio, time.time() * 9 % 360)
        cerchio = cv2.resize(cerchio, (dimensione_settore[0], dimensione_settore[1]))
        regione = immagine[angolo_settore[1]:angolo_settore[1] + dimensione_settore[1], angolo_settore[0]:angolo_settore[0] + dimensione_settore[0], :]

        regione = sovrapponi_immagini(regione, cerchio)
        #immagine = cv2.circle(immagine,
                              #(angolo_settore[0] + int(dimensione_settore[0] / 2),
                              # angolo_settore[1] + int(dimensione_settore[1] / 2)),
                              #dimensione_settore[0] / 3, (0, 255, 0), 3)

        immagine[angolo_settore[1]:angolo_settore[1] + dimensione_settore[1], angolo_settore[0]:angolo_settore[0] + dimensione_settore[0], :] = regione

    else:
        print("WARNING: pezzo is nor X, neither O")

    return immagine


def disegna(immagine, board, angoli_settori, dimensione_settore):
    for i in range(0, 9):
        if board[i] == 'X' or board[i] == 'O':
            immagine = disegna_settore(immagine, board[i], angoli_settori[i], dimensione_settore)

    return immagine


def disegna_fine(immagine, giocatore, posizione_mossa, angoli_settori, dimensioni_settori):
    if giocatore == 'X':
        color = (0, 230, 230)
    else:
        color = (0, 230, 230)

    punto1 = tuple(
        map(operator.add, angoli_settori[posizione_mossa[0]], (dimensioni_settori[0] / 2, dimensioni_settori[1] / 2)))
    punto2 = tuple(
        map(operator.add, angoli_settori[posizione_mossa[1]], (dimensioni_settori[0] / 2, dimensioni_settori[1] / 2)))

    immagine = cv2.line(immagine, punto1, punto2, color, 7)

    return immagine


def sovrapponi_immagini(bg, fg):
    h = np.size(bg, 0)
    w = np.size(bg, 1)
    c = np.size(fg, 2)

    assert (c == 4 and h == np.size(fg, 0) and w == np.size(fg, 1))

    alpha = fg[:, :, 3]
    alpha = alpha / 255
    alpha = alpha[:, :, np.newaxis]
    alpha = np.concatenate((alpha, alpha, alpha), 2)
    bg = np.multiply(bg, (1 - alpha))
    fg1 = fg[:, :, 0:3]
    fg1 = fg1 * alpha
    return bg + fg1


if False:
    rainbow = cv2.imread('/home/francesco/Desktop/rainbow.png', cv2.IMREAD_UNCHANGED)
    mount = cv2.imread('/home/francesco/Desktop/mount.jpg', cv2.IMREAD_UNCHANGED)

    # rainbow = cv2.resize(rainbow, (100, 100))
    # mount = cv2.resize(mount, (100, 100))

    cv2.imshow('a', mount)
    cv2.imshow(' ', rainbow)
    cv2.waitKey()
    cv2.destroyAllWindows()
    while True:
        rainbow_r = imutils.rotate(rainbow, time.time() * 9 % 360)
        im = sovrapponi_immagini(mount, rainbow_r)
        cv2.imshow('gg', im)
        cv2.waitKey(1)
