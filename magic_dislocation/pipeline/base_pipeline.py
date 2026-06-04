"""Base class fora complete pipeline module.

In this module, we define a basic class for a complete pipeline, containing necessay configs, 
functions for loading data, define S plane, selecting data, processing data, and moving data.

  Typical usage example:

  pipeline = BasePipeline(config)
  pipeline.run()
"""


import numpy as np


class BasePipeline:
    """
    This class is the basic pipeline for create dislocation.
    """
    def __init__(self, config):
        self.config = config
        self.positions = config["positions"]
        self.fix_configs()

    
    def run(self):
        raise NotImplementedError


    def load_data(self,):
        raise NotImplementedError


    def select_atoms(self,):
        raise NotImplementedError


    def define_s_plane(self,):
        raise NotImplementedError


    def move_atoms(self,):
        raise NotImplementedError
    
    
    def init_submodules(self,):
        raise NotImplementedError
    
    def fix_configs(self,):
        # move direction vector and layerization direction vector are required
        layerization_direction_vector = np.array(self.config["layer_direction_vector"])
        if "s_init_vertical_axis" not in self.config:   
            if sum(abs(layerization_direction_vector)) == max(abs(layerization_direction_vector)):
                s_init_vertical_axis = np.argmax(abs(layerization_direction_vector))
                s_init_direction_vector = np.zeros(3)
                s_init_direction_vector[s_init_vertical_axis] = 1
                self.config["s_init_vertical_axis"] = s_init_vertical_axis
                self.config["s_init_direction_vector"] = s_init_direction_vector
            else:
                raise ValueError("The layerization_direction_vector is not supported!")
        else:
            s_init_vertical_axis = self.config["s_init_vertical_axis"]
            s_init_direction_vector = np.zeros(3)
            s_init_direction_vector[s_init_vertical_axis] = 1
            self.config["s_init_direction_vector"] = s_init_direction_vector
            
            if (layerization_direction_vector != s_init_direction_vector).any() and "s_direction_vector" not in self.config:
                self.config["s_direction_vector"] = layerization_direction_vector
            
            
            