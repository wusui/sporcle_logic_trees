# Copyright (C) 2024 Warren Usui, MIT License
"""
Convert layouts to a packet formatted in a more friendly manner for the
solver.  The packet returned is a dict with a grid_entry and a color_chart
entry
"""
import os
import string
from itertools import combinations
import get_layouts
import brainz
from html_builder import make_html_file
from get_latest import get_latest
import file_classes

def fix_dup_fig_col(sq_list):
    """
    If there are too few unique colors, find non-touching figures that
    have the same color and slightly modify one.
    """
    fdfc_pkt = list(map(lambda a: [a[0], a[1], False], enumerate(sq_list)))
    fval = {}
    for entry in fdfc_pkt:
        if entry[1] not in fval:
            fval[entry[1]] = entry[0]
            entry[2] = True
    s_size = int(len(sq_list) ** .5)
    old_con = 0
    new_con = len(list(filter(lambda a: a[2], fdfc_pkt)))
    while new_con > old_con:
        for entry in fdfc_pkt:
            def ichk_entry(entv):
                if entv[0] >= s_size:
                    nbor = fdfc_pkt[entv[0] - s_size]
                    if nbor[1] == entv[1] and nbor[2]:
                        entv[2] = True
                if entv[0] <= s_size * (s_size - 1) - 1:
                    nbor = fdfc_pkt[entv[0] + s_size]
                    if nbor[1] == entv[1] and nbor[2]:
                        entv[2] = True
                if entv[0] % s_size != 0:
                    nbor = fdfc_pkt[entv[0] - 1]
                    if nbor[1] == entv[1] and nbor[2]:
                        entv[2] = True
                if entv[0] % s_size != s_size - 1:
                    nbor = fdfc_pkt[entv[0] + 1]
                    if nbor[1] == entv[1] and nbor[2]:
                        entv[2] = True
                return entv
            if entry[2]:
                continue
            entry = ichk_entry(entry)
        old_con = new_con
        new_con = len(list(filter(lambda a: a[2], fdfc_pkt)))
    new_sq = []
    for sq_info in fdfc_pkt:
        if sq_info[2]:
            new_sq.append(sq_info[1])
            continue
        numb = int(sq_info[1][1:], 16)
        if numb % 2 == 0:
            numb += 1
        else:
            numb -= 1
        new_sq.append(f'#{hex(numb)[2:]}')
    return new_sq

def mk_packet(sq_list):
    """
    Test the grid and return False if bad.  If okay, return a dictionary
    where the 'layout' value is representation of the grid with unsolved
    squares still marked with letters.  The 'cchart' value in the
    dictionary is a mapping of a square's letter representation to
    its 24 bit color code.
    """
    def find_closest_cols(hexlist):
        def conv_rgbs(cpart):
            return list(map(lambda a: int(f'0x{a}', 16), cpart))
        def sumdiffs(cvals):
            return sum(list(map(lambda a: abs(cvals[0][a] - cvals[1][a]),
                                [0, 1, 2])))
        mindiff = 1000
        best_so_far = []
        for pair in combinations(hexlist, 2):
            cparts = list(map(lambda a: [a[1:3], a[3:5], a[5:7]], pair))
            cdiff = sumdiffs(list(map(conv_rgbs, cparts)))
            if cdiff < mindiff:
                mindiff = cdiff
                best_so_far = pair
        return list(map(lambda a: best_so_far[1] if a == best_so_far[0]
                        else a, sq_list))
    if int(len(sq_list) ** .5) ** 2 != len(sq_list):
        print('number of cells not a perfect square')
        return []
    rgbv = list(set(sq_list))
    ltoc = list(map(lambda a: [string.ascii_lowercase[a[0]], a[1]],
                    enumerate(rgbv)))
    ctol = dict(list(map(lambda a: [a[1], a[0]], ltoc)))
    grid = ''.join(list(map(lambda a: ctol[a], sq_list)))
    if len(ctol) ** 2 > len(sq_list):
        return mk_packet(find_closest_cols(sorted(ctol)))
    if len(ctol) ** 2 < len(grid):
        return mk_packet(fix_dup_fig_col(sq_list))
    layout = list(map(lambda a: grid[a:a + len(ctol)], range(0, len(grid),
                                                             len(ctol))))
    return {'layout': layout, 'cchart': dict(ltoc)}

def get_pkt_from_json(numb, jsonfiles):
    """
    Read saved grids and extract the grid from the saved_grids json file.
    Pass that grid to mk_packet
    """
    pdict = jsonfiles['grid'].get_data()
    if str(numb) not in pdict:
        return []
    ret_val = mk_packet(pdict[str(numb)])
    if not ret_val:
        print(f'{numb} -- puzzle that probably has issues')
    return ret_val

def get_puz_pkt(number, jsonfiles):
    """
    Either extract data from saved_grids.json or directly from the web page
    """
    cmap = []
    if os.path.exists('saved_grids.json'):
        cmap = get_pkt_from_json(number, jsonfiles)
    if not cmap:
        cmap = mk_packet(get_layouts.get_grid(
            [get_layouts.get_new_gname(number, jsonfiles),
            str(number)], jsonfiles))
        if not cmap:
            print(f'{number} -- puzzle that probably has issues')
    return cmap

def get_puz_pkt_and_sol(number, jsonfiles):
    """
    Main solver entry point
    """
    cmap = get_puz_pkt(number, jsonfiles)
    sol_text = brainz.solver([number, cmap['layout']])
    return [cmap['cchart'], sol_text]

def solve_logic_tree(number, jsonfiles):
    """
    The whole enchilada for one puzzle.  Number is the sporcle game number.
    logic_tree_<number>.html gets created in the html directory
    """
    make_html_file(get_puz_pkt_and_sol(number, jsonfiles))

def do_complete_check():
    """
    Run solve_logic_tree for every puzzle that we can find.
    """
    jsonfiles = file_classes.get_json_files()
    for puzzle in range(1, get_latest() + 1):
        solve_logic_tree(puzzle, jsonfiles)

if __name__ == "__main__":
    do_complete_check()
