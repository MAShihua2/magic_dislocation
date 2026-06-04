"""A base module for adding atoms

In this module, we define a base module for atom adder, containing necessay configs

"""


class BaseAtomAdder:

    def __init__(self, config):
        self.config = config

    def create_atoms(self):
        raise NotImplementedError("The select method is not implemented!")

    def run(self):
        self.create_atoms()