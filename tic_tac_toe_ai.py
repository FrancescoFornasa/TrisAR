# Global variables
huPlayer = 'O'  # human
aiPlayer = 'X'  # ai

test = False


class Move:
    def __init__(self):
        self.index = -1
        self.score = -1


def draw(board):
    print "\n", board[0], " ", board[1], " ", board[2], "\n", board[3], " ", board[4], " ", board[5], "\n", board[6], " ", board[7], " ", board[8], "\n"


def winning(board, player):
    if board[0] == player and board[1] == player and board[2] == player:
        return True, (0, 2)
    if board[3] == player and board[4] == player and board[5] == player:
        return True, (3, 5)
    if board[6] == player and board[7] == player and board[8] == player:
        return True, (6, 8)
    if board[0] == player and board[3] == player and board[6] == player:
        return True, (0, 6)
    if board[1] == player and board[4] == player and board[7] == player:
        return True, (1, 7)
    if board[2] == player and board[5] == player and board[8] == player:
        return True, (2, 8)
    if board[0] == player and board[4] == player and board[8] == player:
        return True, (0, 8)
    if board[2] == player and board[4] == player and board[6] == player:
        return True, (2, 6)

    return False, (0, 0)


def empty_indexes(new_board):
    res = []
    for spot in new_board:
        if spot != huPlayer and spot != aiPlayer:
            res.append(spot)
    return res


def trova_mossa_migliore(new_board, player):
    # available spots
    avail_spots = empty_indexes(new_board)

    # checks for the terminal states such as win, lose, and tie and returning a value accordingly
    controllo_vittoria = winning(new_board, huPlayer)
    if controllo_vittoria[0]:
        m = Move()
        m.score = -10
        return m

    controllo_vittoria = winning(new_board, aiPlayer)
    if controllo_vittoria[0]:
        m = Move()
        m.score = 10
        return m

    if len(avail_spots) == 0:
        m = Move()
        m.score = 0
        return m

    # an array to collect all the objects
    moves = []

    # loop through available spots
    for spot in avail_spots:
        move = Move()
        move.index = new_board[spot]

        # set the empty spot to the current player
        new_board[spot] = player

        # if collect the score resulted from calling minimax on the opponent of the current player
        if player == aiPlayer:
            result = trova_mossa_migliore(new_board, huPlayer)
            move.score = result.score
        else:
            result = trova_mossa_migliore(new_board, aiPlayer)
            move.score = result.score

        # reset the spot to empty
        new_board[spot] = move.index
        moves.append(move)

    # if it is the computer's turn loop over the moves and choose the move with the highest score
    best_move = -1
    if player == aiPlayer:
        best_score = -10000
        i = 0
        while i < len(moves):
            m = moves[i]
            if m.score > best_score:
                best_score = m.score
                best_move = i
            i = i+1

    # else loop over the moves and choose the move with the lowest score
    else:
        best_score = 10000
        i = 0
        while i < len(moves):
            m = moves[i]
            if m.score < best_score:
                best_score = m.score
                best_move = i
            i = i+1

    # return the chosen move (object) from the array to the higher depth
    return moves[best_move]


if test:
    # this is the board flattened and filled with some values to easier asses the Artificial Intelligence.
    origBoard = [0, 1, 2, 3, 4, 5, 6, 7, 8]

    while True:
        draw(origBoard)

        scelta = input("\nInserisci la posizione : ")
        origBoard[scelta] = huPlayer

        if winning(origBoard, huPlayer):
            print("\nHAI VINTO!\n")
            break

        bestSpot = trova_mossa_migliore(origBoard, aiPlayer)
        origBoard[bestSpot.index] = aiPlayer

        if winning(origBoard, aiPlayer):
            print("\nHAI PERSO!\n")
            break

        if len(empty_indexes(origBoard)) == 0:
            print("\nPAREGGIO!\n")
            break
