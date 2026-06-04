""" This module contains the LayerBasedSelector class.

This module contains the LayerBasedSelector class, which is used to select atoms based on the layer.

    Typical usage example:
    
    selector = LayerBasedSelector(config)
    selector.select()

"""


import numpy as np

from .base_selector import BaseSelector


class LayerBasedSelector(BaseSelector):
    
    def __init__(self, config):
        super().__init__(config)
        self.config = config
        self.layer_range = self.config["layer_range"] if "layer_range" in self.config else [0, 1e6]
        
    def select(self):
        """
        Select atoms based on the layer.
        """
        self.layer_atoms = self.config["layer_info"]["layer_atoms"]
        selected_atoms_indexes = []
        for layer, atoms_indexes in self.layer_atoms.items():
            if self.layer_range[0] < layer < self.layer_range[1]:
                selected_atoms_indexes.extend(atoms_indexes)
        return selected_atoms_indexes
        

    def run(self):
        selected_atoms_indexes = self.select()
        result = dict()
        result["selected_atoms_indexes"] = selected_atoms_indexes
        return result