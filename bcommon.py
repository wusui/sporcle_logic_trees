# Copyright (C) 2024 Warren Usui, MIT License
"""
Common routines place where import loops won't cause problems
"""
from functools import reduce
from blobe_wcfaf import blobe_wcfaf
from blobe_remext import blobe_remext
from blobe_combos import blobe_combos

def make_pmap(board):
    """
    Construct map of figure to squares
    """
    pmap = dict(list(map(lambda a: [a, []], list(set(
                reduce(lambda a, b: a + b, board))))))
    if '-' in pmap:
        del pmap['-']
    for row in enumerate(board):
        for col in enumerate(board):
            if board[row[0]][col[0]].islower():
                pmap[board[row[0]][col[0]]].append([row[0], col[0]])
    return pmap

def show_board(board):
    """
    Display board as multiple rows
    """
    rstring = "<BOARD>\n"
    for value in board:
        rstring += f"{value}\n"
    return rstring + '\n'

def do_easy_checks(board, pmap):
    """
    Perform non blobe_pspot checks first
    """
    # Scan for squares that will make other figure filling impossible
    chk0_val = blobe_wcfaf(board, pmap)
    if chk0_val:
        return chk0_val
    # Scan for locations in figures where we know the tree is in another
    # row or column
    chk1_val = blobe_remext(board, pmap)
    if chk1_val:
        return chk1_val
    # Scan for groups of figures with common usable characteristics
    chk2_val = blobe_combos(board, pmap)
    if chk2_val:
        return chk2_val
    return []
