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
Main puzzle solver routine.  Contains main loop collecting data.  Some modules originally here were moved to bcommon.py so that other
modules can use them withouth import loop problems.  Blobe_combos.py, blobe_pspots.py, blobe_remext.py, and blobe_wcfaf.py and bcommon.py
are all called from here to solve puzzles.

### blobe_wcfaf.py
Finds all locations in the puzzle that cannot contain trees because the would cause it to be impossible for another figure to have a tree.

### blobe_remext.py
Finds locations that can not have trees because it has already been determined that the tree used by this figure is in another row or column

### blobe_combos.py
Finds combinations of rows or combinations of columns that allow more locations to be eliminated.  These come in two varieties.  First, if
n figures completely fill n rows or columns, then any square in that figure outside that set of rows or columns can not have a tree.  Second,
if a set of n figures is limited to a set of n rows or columns, then any square insde that set that belongs to another figure can not contain
a tree.

### blobe_pspots.py
If there is a point where none of the above techniques work, then the most connect square is found and tested to see what happens if that
square a tree or an emmpty spot.  This check is rarely needed and happens after all the previous checks have been attempted.

### bcommon.py
Common routines used by brainz.py and the blobe modules.

### html_builder.py
Constructs the Html file that describes how a puzzle was solved.

### get_latest.py
Scans Sporcle site to find the number of the most recently created puzzle

### template.aard
Primitive homegrown template for generating the html file built by html_builder.

## Files created

saved_grids.json stores a dictionary indexed by puzzle number where each entry is a list of squares in that puzzle.  Cteated by running
get_layouts.py

html is a local directory where solutions named logic_tree_<number>.html are stored.  All logic tree puzzles are solved by
running get_puz_input.py



