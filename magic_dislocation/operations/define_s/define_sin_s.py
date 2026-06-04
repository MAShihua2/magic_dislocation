""" 
    In this moduele, we define a class for defining a rectangle S plane based on the given config.

    Typical usage example:

    define_s = DefineSinS(config)
    define_s.run()
"""

import numpy as np

from .base_define_s import BaseDefineS


class DefineSinS(BaseDefineS):
    
    def __init__(self, config):
        super().__init__(config)
        self.s_length = self.config["s_length"]
        self.s_width = self.config["s_width"]
        self.s_A = self.config["s_A"]
        self.s_omega = self.config["s_width"]
        self.s_num_points = self.config["s_num_points"]
        self.s_start = self.config["s_start"]
        self.s_end = self.config["s_end"]
        self.s_init_vertical_axis = self.config["s_init_vertical_axis"]
        self.s_center_point = self.config["s_center_point"]
        self.lattice = self.config["lattice"]
        self.s_direction_vector = self.config["s_direction_vector"] if "s_direction_vector" in self.config else None
        self.s_init_direction_vector = self.config["s_init_direction_vector"] if "s_init_direction_vector" in self.config else None


    def get_rectangle_points(self):
        """
        Get the edge points of the S plane.
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
    
    def get_insert_edge_points(self, edge_points, insert_index, extra_points):
        new_edge_points = []
        for i, item in enumerate(edge_points):
            new_edge_points.append(list(item))
            if i == insert_index:
                new_edge_points += extra_points
        return np.array(new_edge_points)
    
    def get_vertex_points(self):
        """
        Get the vertex points of the S plane.
        """
        # prepare the rectangle points
        rectangle_points = self.get_rectangle_points()
        
        # prepare the sin points
        self.s_start_point = rectangle_points[self.s_start]
        self.s_end_point = rectangle_points[self.s_end]
        theta_list = list(np.linspace(np.pi / 4, 2 * np.pi + np.pi / 4, self.s_num_points))
        delta_index = np.argmax(abs(self.s_end_point - self.s_start_point))
        delta_values = list(np.linspace(self.s_start_point[delta_index], self.s_end_point[delta_index], self.s_num_points))
        sin_values = [self.s_A * np.sin(self.s_omega * theta) for theta in theta_list]

        points = []
        for i in range(self.s_num_points):
            tmp_pos = [0, 0, 0]
            tmp_pos[delta_index] = delta_values[i]
            tmp_pos[self.s_init_vertical_axis] = self.s_center_point[self.s_init_vertical_axis]
            res_index = [0, 1, 2]
            res_index.remove(delta_index)
            res_index.remove(self.s_init_vertical_axis)
            res_index = res_index[0]
            tmp_pos[res_index] = sin_values[i]
            points.append(tmp_pos)
        
        # merge the points
        merged_points = self.get_insert_edge_points(rectangle_points, self.s_start, points)

        return np.array(merged_points)
    
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