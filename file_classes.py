# Copyright (C) 2024 Warren Usui, MIT License
"""
Manage the updating of the grid file and the two exceptions files.
"""
import json
import weakref

class Tfile:
    """
    Organize updating of json files used by the logic trees solver
    """
    def __init__(self, in_file):
        self.fname = in_file
        with open(in_file, 'r', encoding='utf-8') as fp_trees:
            self.data = json.loads(fp_trees.read())
        self.weakref_smph = self
        weakref.finalize(self.weakref_smph, self.we_are_done)

    def we_are_done(self):
        """
        Update json file up completion
        """
        with open(self.fname, 'w', encoding='utf-8') as fp_trees:
            json.dump(dict(sorted(self.data.items())), fp_trees, indent=4)

    def add_new_entry(self, keyv, new_data):
        """
        Update an entry
        """
        self.data[keyv] = new_data

    def get_data(self):
        """
        Wrapper to access saved data
        """
        return self.data

def get_json_files():
    """
    Externally callable way of getting the json files.
    """
    return {'grid': Tfile('saved_grids.json'),
            'diff': Tfile('different_names.json'),
            'vdif': Tfile('very_different_names.json')}
