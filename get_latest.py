# Copyright (C) 2024 Warren Usui, MIT License
"""
Find the most recently created logic trees puzzle
"""
from selenium import webdriver

def get_latest():
    """
    Find the tree value returned by the script
    """
    urlhead = 'https://www.sporcle.com/user/Katie_Wandering/quizzes/'
    urlquery = 'order_by=user-released'
    url = '?'.join([urlhead, urlquery])
    opts = webdriver.ChromeOptions()
    opts.add_argument("headless")
    driver = webdriver.Chrome(options=opts)
    driver.get(url)
    treelist = driver.execute_script("return app.payload.listRows")
    for entry in treelist:
        if entry['game_name'].startswith('Trees Logic Puzzle'):
            return int(entry['game_name'].split()[-1])
    return 1
