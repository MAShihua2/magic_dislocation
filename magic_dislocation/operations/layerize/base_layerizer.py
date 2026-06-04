""" A base module for layerizer

In this module, we define a base module for layerizer, containing necessay configs

"""

class BaseLayerizer:

    def __init__(self, config):
        self.config = config

    def layerize(self):
        raise NotImplementedError("The layerize method is not implemented!")

    def run(self):
        return self.layerize()