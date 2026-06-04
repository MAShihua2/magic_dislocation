""" A base module for moving atoms

In this module, we define a base module for moving atoms, containing necessay configs,
"""

class BaseMover:

    def __init__(self, config):
        self.config = config

    def move(self):
        raise NotImplementedError("The move method is not implemented!")

    def run(self):
        return self.move()