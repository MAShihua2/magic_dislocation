""" 
    In this moduele, we define a class for defining a rectangle S plane based on the given config.

    Typical usage example:
    
    define_s = DefineLoopS(config)
    define_s.run()
"""

import numpy as np

from .base_define_s import BaseDefineS


class DefineLoopS(BaseDefineS):
    
    def __init__(self, config):
        super().__init__(config)
        self.s_center_point = self.config["s_center_point"]
        self.s_type = self.config["s_type"]
        self.s_radius = self.config["s_radius"]
        self.s_num_points = self.config["s_num_points"]
        self.s_init_vertical_axis = self.config["s_init_vertical_axis"]
        self.lattice = self.config["lattice"]
        self.s_direction_vector = self.config["s_direction_vector"] if "s_direction_vector" in self.config else None
        self.s_init_direction_vector = self.config["s_init_direction_vector"] if "s_init_direction_vector" in self.config else None
        
        
    def get_vertex_points(self):
        """
        Get the vertex points of the S plane.
        """
        vertex_points = []

        S_R = self.s_radius * self.lattice
        theta_list = list(np.linspace(0, 2 * np.pi, self.s_num_points+1))
        vertex_points = [[S_R * np.cos(theta) if abs(S_R * np.cos(theta)) > 1e-8 else 0,
                   S_R * np.sin(theta) if abs(S_R * np.sin(theta)) > 1e-8 else 0
                  ] for theta in theta_list]
        
        for i, point in enumerate(vertex_points):
            point.insert(self.s_init_vertical_axis, 0)
            point[0] += self.s_center_point[0]
            point[1] += self.s_center_point[1]
            point[2] += self.s_center_point[2]
        
        vertex_points = np.array(vertex_points)
        
        return vertex_points
    
    
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