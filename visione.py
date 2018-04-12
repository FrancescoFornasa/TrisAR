import cv2


def osserva_settore(roi):
    # TODO
    return ' '


def guarda_griglia(warped_frame, posizioni_angoli, dimensione_settore):

    board = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    while i < len(posizioni_angoli):
        angolo = posizioni_angoli[i]
        valore = osserva_settore(warped_frame[angolo[0]:angolo[0]+dimensione_settore[0], angolo[1]:angolo[1]+dimensione_settore[1]])
        if valore != ' ':
            board[i] = valore
        i = i+1

    return board







