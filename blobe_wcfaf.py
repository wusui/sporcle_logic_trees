# Copyright (C) 2024 Warren Usui, MIT License
"""
Find locations where a tree would make it impossible to place a tree in
another figure.
"""
def blobe_wcfaf(board, pmap):
    """
    wcfaf --> would completely fill another figure.
    board -- logic tree layout
    pmap -- dict indexed by figure label.  Values are lists of coordinates
            in that figure
    """
    loc_wo_fig = []
    def rowscan(row):
        def colscan(col):
            def near_chk(figv):
                return row[0] == figv[0] or col[0] == figv[1] or (
                        abs(row[0] - figv[0]) == 1 and
                        abs(col[0] - figv[1]) == 1)
            if board[row[0]][col[0]].islower():
                for fig in pmap:
                    if fig == board[row[0]][col[0]]:
                        continue
                    if not pmap[fig]:
                        continue
                    nearv = list(filter(near_chk, pmap[fig]))
                    if len(nearv) == len(pmap[fig]):
                        loc_wo_fig.append([row[0], col[0], fig])
                        break
        _ = list(map(colscan, enumerate(board)))
    _ = list(map(rowscan, enumerate(board)))
    if loc_wo_fig:
        answer = '<TEXT 1>\n'
        for entry in loc_wo_fig:
            templ = list(board[entry[0]])
            templ[entry[1]] = '-'
            board[entry[0]] = ''.join(templ)
            answer += f'{entry[0] + 1}, {entry[1] + 1} cannot have a tree'
            answer += ' because you then cannot have a tree in'
            answer += f' figure {entry[2]}\n'
        return [board, answer]
    return []
