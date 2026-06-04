""" A base module for layerizer based on given direction vector

In this module, we define a base module for layerizer based on given direction vector, containing necessay configs,

"""


import numpy as np
from .base_layerizer import BaseLayerizer

class VectorBasedLayerizer(BaseLayerizer):

    def __init__(self, config):
        super().__init__(config)
        self.direction_vector = self.config["layer_direction_vector"]
        # self.tolerance = self.config["tolerance"]
        self.positions = self.config["positions"]


    def layerize(self):
        """
        Layerize atoms based on the given direction vector.
        """
        delta_vector = self.positions - self.direction_vector

        projection = np.dot(delta_vector, self.direction_vector) / np.linalg.norm(self.direction_vector)
        projection = np.round(projection, 0)
        
        result = dict()
        
        for i, proj in enumerate(projection):
            if proj not in result:
                result[proj] = []
            result[proj].append(i)

        for key in result:
            result[key] = np.array(result[key])
            
        sorted_proj_dict = dict(sorted(result.items()))
        
        for key in sorted_proj_dict:
            sorted_proj_dict[key] = np.array(sorted_proj_dict[key])
            
        atoms_layer_key_dict = dict()
        for i, key in enumerate(sorted_proj_dict):
            atoms_layer_key_dict[i] = sorted_proj_dict[key]
            
        result["layer_projection"] = projection
        result["layer_projection_atoms"] = sorted_proj_dict
        result["layer_atoms"] = atoms_layer_key_dict
        
        final_result = dict()
        final_result["layer_info"] = result
        return final_result