# Copyright (C) 2024 Warren Usui, MIT License
"""
Scan for Sporcle logic tree grid layouts.  A layout is a list of hex
RGB values corresponding to the colors in a logic tree square.  The
values in the list are scanned left to right, top to bottom from the
square.
"""
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from get_latest import get_latest
import file_classes

def get_puzzle(numb, vdiff):
    """
    Given a number, return the url of the logic tree webpage
    """
    if numb in vdiff:
        return '/'.join(['https://www.sporcle.com/games/Katie_Wandering',
                    vdiff[numb]])
    #if numb == '240':
    #    return '/'.join(['https://www.sporcle.com/games/Katie_Wandering',
    #                'woo-my-400th-quiz'])
    #if numb == '500':
    #    return '/'.join(['https://www.sporcle.com/games/Katie_Wandering',
    #                '500-trees-logic-puzzles'])
    return '/'.join(['https://www.sporcle.com/games',
                    f'Katie_Wandering/trees-logic-puzzle-{numb}'])

def adj_numb(number, bad_sporcle):
    """
    Adjust the value of a number tacked onto a url.  Handle one off
    cases due to Sporcle inconsistencies.
    """
    #bad_sporcle = {29: 'xxvix', 102: '103-1', 160: '160-1', 183: '183-1',
    #               63: 'lxiii', 68: 'lxviii', 73: 'lxxiii', 204: '204-1',
    #               205: '205-1', 282: '282-1', 291: '291-1', 329: '329-1',
    #               344: '344-1', 388: '388-1', 484: '484-1', 485: '485-1',
    #               638: '638-1'}
    def romanize():
        def one_digit(lowdig):
            if lowdig % 5 == 4:
                return ''.join(['i', ['v', 'x'][lowdig // 5]])
            return ''.join([lowdig // 5 * 'v', lowdig % 5 * 'i'])
        return ''.join([number // 10 * 'x', one_digit(number % 10)])
    if str(number) in bad_sporcle:
        return bad_sporcle[str(number)]
    if number < 40:
        return romanize()
    return f'{number}'

def get_new_gname(numb, jsonfiles):
    """
    Wrapper to extract a logic tree give an integer value for that tree
    """
    return get_puzzle(adj_numb(numb, jsonfiles['diff'].get_data()),
                      jsonfiles['vdif'].get_data())

def get_grid(urldata, jsonfiles):
    """
    Main data extraction routine.  Scan the innerhtml of the grid-container
    and extract the rgb value for each square.  Return values in a list.
    """
    def mk_ints(crgbv):
        return list(map(int, crgbv[0:3]))
    def get_hex(rgb_info):
        return f"#{''.join(list(map(lambda a: f'{a:02x}', rgb_info)))}"
    opts = webdriver.ChromeOptions()
    opts.add_argument("headless")
    driver = webdriver.Chrome(options=opts)
    driver.get(urldata[0])
    time.sleep(2)
    gwrap = driver.find_element(By.ID, "grid-container")
    grid_data = gwrap.get_attribute("innerHTML")
    soup = BeautifulSoup(grid_data, 'html.parser')
    bgcols = soup.find_all('div', class_="bg-color")
    str_style = list(map(lambda a: a['style'], bgcols))
    str_nums = list(map(lambda a: a.split('(')[-1].split(')')[0], str_style))
    str_rgb = list(map(lambda a: a.split(','), str_nums))
    str_rgb_int = list(map(mk_ints, str_rgb))
    out_grid_data = list(map(get_hex, str_rgb_int))
    jsonfiles['grid'].add_new_entry(urldata[1], out_grid_data)
    return out_grid_data

def get_tree_grid(numb, jsonfiles):
    """
    For the puzzle number given, get the grid layout.  Entry point to extract
    rgb list for one numbered puzzle.
    """
    print(f'Extracting data from web for puzzle: {numb}')
    return get_grid([get_new_gname(numb, jsonfiles), str(numb)], jsonfiles)

def populate_games():
    """
    Stash a bunch of grid layouts.  Data gets written out when the
    program terminates because of a weakref finalizer set for the
    json files.
    """
    jsonfiles = file_classes.get_json_files()
    return dict(list(map(lambda a: [a, get_tree_grid(a, jsonfiles)],
                          range(1, get_latest() + 1))))

if __name__ == "__main__":
    populate_games()
