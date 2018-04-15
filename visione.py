import cv2
import numpy as np
import tic_tac_toe_ai as ai
import operator

soglia = 2  # soglia alta fa piu falsi positivi


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
        valore = osserva_settore(warped_frame[angolo[1]:angolo[1]+dimensione_settore[1], angolo[0]:angolo[0]+dimensione_settore[0]])

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
                                  (angolo_settore[0]+int(dimensione_settore[0]/2), angolo_settore[1]+int(dimensione_settore[1]/2)),
                                  (0, 0, 255), cv2.MARKER_TILTED_CROSS, int(dimensione_settore[0]/2) , 3)
    elif pezzo == 'O':
        immagine = cv2.circle(immagine,
                              (angolo_settore[0]+int(dimensione_settore[0]/2), angolo_settore[1]+int(dimensione_settore[1]/2)),
                              dimensione_settore[0]/3, (0, 255, 0), 3)

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

    punto1 = tuple(map(operator.add, angoli_settori[posizione_mossa[0]], (dimensioni_settori[0]/2, dimensioni_settori[1]/2)))
    punto2 = tuple(map(operator.add, angoli_settori[posizione_mossa[1]], (dimensioni_settori[0]/2, dimensioni_settori[1]/2)))

    immagine = cv2.line(immagine, punto1, punto2, color, 7)

    return immagine




























