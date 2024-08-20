# Copyright (C) 2024 Warren Usui, MIT License
"""
If all other checks fail, see what happens if a key square is empty or a
tree.  The key square is the square that interacts with the most diagonal
neighbors and is in the smallest sized figure.
"""
from copy import deepcopy
from bcommon import make_pmap, do_easy_checks

def set_board_vnot(board, entry):
    """
    General set a board value routine
    """
    templ = list(board[entry[0]])
    templ[entry[1]] = '-'
    board[entry[0]] = ''.join(templ)
    return board

def isbadb(board):
    """
    Find a row or column that is all empty
    """
    def isb(bline):
        return list(filter(lambda a: a != '-', list(bline)))
    oval = list(filter(lambda a: len(a) > 0, list(map(isb, board))))
    return len(oval) < len(board[0])

def loc_update(board, entry, ttype):
    """
    Update board locally (used to test effects of changes in grid)
    """
    if ttype == '-':
        board = set_board_vnot(board, entry)
    else:
        for row in range(len(board[0])):
            for col in range(len(board[0])):
                if row == entry[0] and col == entry[1]:
                    continue
                if row == entry[0]:
                    board = set_board_vnot(board, [row, col])
                if col == entry[1]:
                    board = set_board_vnot(board, [row, col])
                if abs(row - entry[0]) == 1 and abs(col - entry[1]) == 1:
                    board = set_board_vnot(board, [row, col])
    while True:
        pmap = make_pmap(board)
        chk_inf = do_easy_checks(board, pmap)
        if not chk_inf:
            break
        board = chk_inf[0]
    return board

def  blobe_pspots(board, pmap):
    """
    Find the best squares to test and see what happens when Tree values of
    empty values are set here.
    """
    # problem spots are squares with most diagonal neighbors in smallest fig
    def find_best_sq():
        orating = 0
        obsq = []
        for fig in pmap:
            def aint_valid(numb):
                return numb < 0 or numb >= len(board[0])
            for sqc in pmap[fig]:
                nvals = []
                for xoff in [-1, 1]:
                    xval = sqc[0] + xoff
                    if aint_valid(xval):
                        continue
                    for yoff in [-1, 1]:
                        yval = sqc[1] + yoff
                        if aint_valid(yval):
                            continue
                        if board[xval][yval] != '-' and \
                                            board[xval][yval] != fig:
                            nvals.append(board[xval][yval])
                ccount = len(list(set(nvals)))
                rating = ccount * len(board[0]) * len(board[0]) \
                                    - len(pmap[fig])
                if rating > orating:
                    orating = rating
                    obsq = sqc
        return obsq
    obsq = find_best_sq()
    result_tree = loc_update(deepcopy(board), obsq, 'T')
    answer = '<TEXT 5>\n'
    if isbadb(result_tree):
        board = set_board_vnot(board, obsq)
        answer += f'A tree in row {obsq[0] + 1}, column {obsq[1] + 1} '
        answer += 'will result in an invalid board\n'
        answer += f'\t{obsq[0] + 1}, {obsq[1] + 1} cannot have a tree\n'
    else:
        answer += f'An empty row {obsq[0] + 1}, column {obsq[1] + 1} '
        answer += 'will result in an invalid board\n'
        answer += f'\t{obsq[0] + 1}, {obsq[1] + 1} must have a tree\n'
        for row in range(len(board[0])):
            for col in range(len(board[0])):
                if board[row][col] != '-':
                    board = set_board_vnot(board, [row, col])
                    answer += f'\t\t{row}, {col} cannot have a tree\n'
    return [board, answer]
