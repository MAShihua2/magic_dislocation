"""A base module for deleting atoms

In this module, we define a base module for atom deleter, containing necessay configs,
    
"""

import os

import ase


class BaseAtomDeleter:

    def __init__(self, config):
        self.config = config

    def select_atoms(self):
        raise NotImplementedError("The select method is not implemented!")

    def run(self):
        self.select_atoms()