# Logic Trees

Solve logic trees puzzles found on Sporcle webesite.

## Contents

### get_layouts.py
Scrapes the starting game information from the web page.  It uses selenium and returns a list of hex color values
representing the colors of the squares in the starting game.  This can be either used directly or can be stored in a json file
indexed by game number.  Populate_games() stores the first 200 game starting positions in the saved_grids.json file stored in the
local directory.  Get_tree_grid(numb) extracts the list of square colors for the game number specified by numb.  Other code in
this file handles inconsistencies found in the naming of Sporcle files.
 
### get_puz_input.py
Takes the data from get_layouts and reformats it in a manner more suited for other functions.  The main function is mk_packet, which
takes the list of colors and returns a dictionary containing two items: 'layout' where color data is formatted into a list of strings
where each string represents a row of the puzzle and each character in the string is a corresponding square in the puzzle.  A letter
is substituted for each color.  'cchart' is the second item which is dictionary of color values indexed by the corresponding character
in the layout.  Other functions include various combinations that call solving and display functions.  Solve_logic_tree(number) is a
one-stop shop that takes a puzzle number and produces an html page for the solution.

### brainz.py
Main puzzle solver routine.

