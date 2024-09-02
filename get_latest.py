# Copyright (C) 2024 Warren Usui, MIT License
"""
Find the most recently created logic trees puzzle
"""
from selenium import webdriver
import file_classes

def get_all_latest_trees():
    """
    Find most recent tree values.
    """
    urlhead = 'https://www.sporcle.com/user/Katie_Wandering/quizzes/'
    urlquery = 'order_by=user-released'
    url = '?'.join([urlhead, urlquery])
    opts = webdriver.ChromeOptions()
    opts.add_argument("headless")
    driver = webdriver.Chrome(options=opts)
    driver.get(url)
    treelist = driver.execute_script("return app.payload.listRows")
    return list(filter(lambda a: a['game_name'].startswith(
            'Trees Logic Puzzle '), treelist))

def get_latest():
    """
    Find highest tree puzzle number
    """
    return int(get_all_latest_trees()[0]['game_name'].split()[-1])

def edit_diff_files(new_files, jsonfiles):
    """
    Find unusually formatted new quiz file names and set entries for these
    in the appropriate json files.
    """
    odd_names = list(filter(lambda a: f'trees-logic-puzzle-{a[0]}' !=
                            a[1], new_files))
    if not odd_names:
        return
    for entry in odd_names:
        print(entry[0], entry[1])
        if entry[1].startswith('trees-logic-puzzle-'):
            jsonfiles['diff'].add_new_entry(entry[0],
                        entry[1][len('trees-logic-puzzle-'):])
        else:
            jsonfiles['vdif'].add_new_entry(entry[0], entry[1])

def get_unsaved_puzzles(jsonfiles):
    """
    Update values in the different_names.json and very_different_names.json
    files as new quizzes get added.
    """
    new_trees = get_all_latest_trees()
    new_entries = []
    for entry in new_trees:
        enumb = entry['game_name'].split()[-1]
        if enumb in jsonfiles['grid'].data:
            break
        new_entries.append(entry)
    if not new_entries:
        return
    pnumbs = list(map(lambda a: a['game_name'].split(' ')[-1], new_entries))
    urlvals = list(map(lambda a: a['game_url'].split('/')[-1], new_entries))
    edit_diff_files(list(zip(pnumbs, urlvals)), jsonfiles)

def find_inconsistent_names():
    """
    Get data from json files and update information for new puzzles
    """
    get_unsaved_puzzles(file_classes.get_json_files())

if __name__ =="__main__":
    find_inconsistent_names()
