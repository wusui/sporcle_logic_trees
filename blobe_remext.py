# Copyright (C) 2024 Warren Usui, MIT License
"""
Find locations external to a row or column where it is known that a
figures tree exists.
"""
def  blobe_remext(board, pmap):
    """
    TO DO: Expand to multiple rows/columns
    """
    def commond(ltype):
        switcher = {'row': 0, 'col': 1}
        words = {'row': 'row', 'col': 'column'}
        com_chk = []
        def column(cindx):
            return list(map(lambda a: a[cindx], board))
        def rcscan(rcv):
            answer = '<TEXT 2>\n'
            if ltype == 'row':
                rlist = list(filter(lambda a: a != '-', list(board[rcv[0]])))
            else:
                rlist = list(filter(lambda a: a != '-', column(rcv[0])))
            if len(list(set(rlist))) == 1:
                if len(pmap[rlist[0]]) > 1:
                    for entry in pmap[rlist[0]]:
                        if entry[switcher[ltype]] != rcv[0]:
                            com_chk.append(entry)
                if len(com_chk) > 0:
                    dpoints = board[com_chk[0][0]][com_chk[0][1]]
                    answer += f'figure {dpoints} must have a tree in '
                    answer += f'{words[ltype]} {rcv[0] + 1}\n'
                    for entry in com_chk:
                        templ = list(board[entry[0]])
                        templ[entry[1]] = '-'
                        board[entry[0]] = ''.join(templ)
                        answer += f'\t{entry[0] + 1}, {entry[1] + 1}'
                        answer += ' cannot have a tree\n'
            return [board, answer]
        com_chk = list(filter(lambda a: len(a[1]) != len("<TEXT X>\n"),
                        list(map(rcscan, enumerate(board)))))
        if com_chk:
            return com_chk[0]
        return []
    value = commond('row')
    if value:
        return value
    value = commond('col')
    if value:
        return value
    return []
