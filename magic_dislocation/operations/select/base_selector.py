"""A base module for selector

In this module, we define a base module for selector, containing necessay configs,
"""


class BaseSelector:

    def __init__(self, config):
        self.config = config

    def select(self):
        raise NotImplementedError("The select method is not implemented!")

    def run(self):
        self.select()