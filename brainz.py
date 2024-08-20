# Copyright (C) 2024 Warren Usui, MIT License
"""
Find solutions
"""
from functools import reduce
from bcommon import make_pmap, do_easy_checks, show_board
from blobe_pspots import blobe_pspots

def check_input(board):
    """
    Make sure board is legit
    """
    sq_dim = len(board[0])
    if len(list(filter(lambda a: len(a) == sq_dim, board))) != sq_dim:
        print("Invalid number of properly sized rows")
        return []
    if len(list(filter(lambda a: a not in
                'abcdefghijklmnopqrstuvwxyz'[0:sq_dim],
                reduce(lambda a, b: a + b, board)))) > 0:
        print("Invalid square value found")
        return []
    return board

def update(board):
    """
    Main testing routine.
        1. First make sure we get rid of squares that cannot have
           trees because trees in these locations will make other
           figures unable to have any trees
        2. Next remove trees from locations that are not in rows or
           columns where we know a tree will occur
    This process iterates by starting from the beginning so new changes
    made will be caught and used for processing
    """
    pmap = make_pmap(board)
    chk_inf = do_easy_checks(board, pmap)
    if chk_inf:
        return chk_inf
    chk3_val = blobe_pspots(board, pmap)
    if chk3_val:
        return chk3_val
    return [list(map(lambda a: a.upper(), board)), '<TEXT 0> Incomplete\n']

def still_not_solved(board):
    """
    Doneness check in solver
    """
    return len(list(filter(lambda a: a.islower(),
                    reduce(lambda a, b: a + b, board)))) > len(board)

def solver(in_data):
    """
    Solver entry point
    """
    story_log = f'<TITLE>\nLogic tree number {in_data[0]}\n'
    board = check_input(in_data[1])
    story_log += show_board(board)
    ret_data = ''
    while still_not_solved(board):
        ret_data = update(board)
        board = ret_data[0]
        story_log += (ret_data[1] + show_board(ret_data[0]))
    story_log += ('<TEXT 9>\nFinal Grid\n' + show_board(ret_data[0]))
    print(f'Solved quiz {in_data[0]}')
    return story_log
