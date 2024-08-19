# Copyright (C) 2024 Warren Usui, MIT License
"""
Handle multiline cases (two varieties explained below)
"""
from itertools import chain, combinations, product

def rc_text(numb):
    """
    Minor text output fixer
    """
    return {0: 'row', 1: 'column'}[numb]

def lfmt(olist):
    """
    Format lists to include an and and an Oxford comma
    """
    def fmt2(list2):
        return list2[0:-1] + ['and'] + [list2[-1]]
    if isinstance(olist[0], int):
        olist = list(map(lambda a: a + 1, olist))
    parts = fmt2(list(map(str, olist)))
    back = parts[-2:]
    front = parts[0:-2]
    if len(front) < 2:
        return ' '.join(parts)
    front = list(map(lambda a: a + ',', front))
    return ' '.join(front + back)

def set_line_types(chart):
    """
    Set noise (lines with only one group entry), and clines (common lines)
    """
    cmap = {}
    for lindx in chart:
        for numb in chart[lindx]:
            if numb in cmap:
                cmap[numb].append(lindx)
            else:
                cmap[numb] = [lindx]
    noise = []
    clines = []
    for lindx, cmapobj in cmap.items():
        if len(cmapobj) == 1:
            noise.append(lindx)
        else:
            clines.append(lindx)
    return noise, clines

def blobe_combos(board, pmap):
    """
    Main processing of multiple line combinations.  The smaller the
    combination, the earlier it is found/used.  There are two possible
    cases for finding squares that do not have trees.  One case happens
    when the location of the trees are isolated to certain rows/columns
    of a figure.  This allows us to remove the squares that are not in
    those rows or columns.  The second case happens when the trees are
    isolated to a set of rows/columns, there are no other external
    points in the figures, and the size of the area is the exact size
    of the number of trees needed for the set of figures.  In this case,
    we can remove all squares that are not in the area that are not in
    the combination
    """
    def find_combos(matchup, indx):
        def get_indx(coords):
            return list(set(list(map(lambda a: a[indx], coords))))
        alines = list(map(get_indx, list(map(lambda a: pmap[a], matchup))))
        noise, clines = set_line_types(dict(zip(matchup, alines)))
        def ulinetest():
            def lchk(cline):
                if indx == 0:
                    chkr = list(board[cline])
                else:
                    chkr = list(map(lambda a: a[cline], board))
                other = list(filter(lambda a: a not in list(matchup) + ['-'],
                                   chkr))
                if len(other) > 0:
                    return False
                return True
            return list(filter(lchk, clines))
        ulines = ulinetest()
        if len(ulines) == len(matchup):
            if len(ulines) != len(clines) or len(noise) > 0:
                answer = "<TEXT 3>\n"
                answer += f'{rc_text(indx).title()}s, {lfmt(ulines)} '
                answer += f'must contain trees for figures {lfmt(matchup)}\n'
                answer += f'Therefore, {lfmt(matchup)} figures cannot '
                answer += f'contain trees in other {rc_text(indx)}s\n'
                all_pts = list(chain.from_iterable(
                        list(map(lambda a: pmap[a], matchup))))
                del_pts = list(filter(lambda a: a[indx] not in ulines,
                                      all_pts))
                for entry in del_pts:
                    answer += f'\t{entry[0] + 1}, {entry[1] + 1}'
                    answer += ' cannot have a tree\n'
                    templ = list(board[entry[0]])
                    templ[entry[1]] = '-'
                    board[entry[0]] = ''.join(templ)
                return [board, answer]
        if len(clines) == len(matchup):
            if len(noise) == 0 and len(clines) != len(ulines):
                answer = "<TEXT 4>\n"
                answer += f'{rc_text(indx).title()}s, {lfmt(clines)} '
                answer += f'must contain trees for figures {lfmt(matchup)}\n'
                answer += 'Therefore, no trees can be in '
                answer += f'{rc_text(indx)}s, {lfmt(clines)} that are not in '
                answer += f'{lfmt(matchup)}\n'
                if indx == 1:
                    all_pts = product(list(range(len(board[0]))), clines)
                else:
                    all_pts = product(clines, list(range(len(board[0]))))
                for entry in all_pts:
                    if board[entry[0]][entry[1]] == '-':
                        continue
                    if board[entry[0]][entry[1]] in matchup:
                        continue
                    answer += f'\t{entry[0] + 1}, {entry[1] + 1}'
                    answer += ' cannot have a tree\n'
                    templ = list(board[entry[0]])
                    templ[entry[1]] = '-'
                    board[entry[0]] = ''.join(templ)
                return [board, answer]
        return []
    ufigs = list(filter(lambda a: len(pmap[a]) > 1, pmap))
    for count in range(2, min(5, len(ufigs))):
        figs = list(combinations(ufigs, count))
        for matchup in figs:
            for indx in range(0, 2):
                bval = find_combos(matchup, indx)
                if bval:
                    return bval
    return []
