""" 
    In this moduele, we define a class for defining a rectangle S plane based on the given config.

    Typical usage example:

    define_s = DefineRectangleS(config)
    define_s.run()
"""

import numpy as np

from .base_define_s import BaseDefineS


class DefineRectangleS(BaseDefineS):
    
    def __init__(self, config):
        super().__init__(config)
        self.s_length = self.config["s_length"]
        self.s_width = self.config["s_width"]
        self.s_init_vertical_axis = self.config["s_init_vertical_axis"]
        self.lattice = self.config["lattice"]
        self.s_direction_vector = self.config["s_direction_vector"] if "s_direction_vector" in self.config else None
        self.s_init_direction_vector = self.config["s_init_direction_vector"] if "s_init_direction_vector" in self.config else None
        
        
    def get_vertex_points(self):
        """
        Get the vertex points of the S plane.
        """
        vertex_points = []
        center_pos = self.s_center_point
        
        if self.s_init_vertical_axis == 2:
            operator_list = [[-self.s_length/2, self.s_width/2, 0], [self.s_length/2, self.s_width/2, 0], 
                             [self.s_length/2, -self.s_width/2, 0], [-self.s_length/2, -self.s_width/2, 0]]
        elif self.s_init_vertical_axis == 1:
            operator_list = [[-self.s_length/2, 0, self.s_width/2], [self.s_length/2, 0, self.s_width/2], 
                             [self.s_length/2, 0, -self.s_width/2], [-self.s_length/2, 0, -self.s_width/2]]
        elif self.s_init_vertical_axis == 0:
            operator_list = [[0, -self.s_length/2, self.s_width/2], [0, self.s_length/2, self.s_width/2], 
                             [0, self.s_length/2, -self.s_width/2], [0, -self.s_length/2, -self.s_width/2]]

        vertex_points =  [center_pos + oper  for oper in operator_list]
        
        return np.array(vertex_points)
    
    
    def define_s(self):
        """
        Define the S plane.
        """
        
        results = {"s_center_point": self.s_center_point}

        vertex_points = self.get_vertex_points()
        
        results["vertex_points"] = vertex_points
        
        if self.s_direction_vector is not None: # if need to rotate to a non-axis plane
            results["init_vertex_points"] = vertex_points.copy()
            rotated_vertex_points = self.rotate_S_plane(vertex_points, self.s_center_point, 
                                                self.s_init_vertical_axis, 
                                                self.s_init_direction_vector, 
                                                self.s_direction_vector)
            results["rotated_vertex_points"] = rotated_vertex_points
            results.pop("vertex_points")
        
        return results