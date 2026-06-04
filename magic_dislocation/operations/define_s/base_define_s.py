"""A base module for define_s

In this module, we define a base module for defining S plane, containing necessay configs
"""

import numpy as np

from magic_dislocation.utils import get_rotation_info


class BaseDefineS:

    def __init__(self, config):
        self.config = config
        self.s_center_point = self.config["s_center_point"]
        self.s_type = self.config["s_type"]

    def run(self):
        resutls = self.define_s()
        return resutls
        
    def define_s(self):
        raise NotImplementedError("The define_s method is not implemented!")
    

    def rotate_S_plane(self, s_edge_points, s_center_point, s_init_vertical_axis, insert_plane, target_plane):
        rotation_matrix = get_rotation_info(insert_plane, target_plane)
        
        # for s_tri_point in s_edge_points:
        #     s_tri_point[s_init_vertical_axis] -= s_center_point[s_init_vertical_axis]
        #     trans_pos = np.dot(rotation_matrix, s_tri_point.reshape(-1, 1))
        #     trans_pos[s_init_vertical_axis] += s_center_point[s_init_vertical_axis]
        #     s_tri_point[0:] = trans_pos.reshape(-1)

        for s_tri_point in s_edge_points:
            s_tri_point -= s_center_point
            trans_pos = np.dot(rotation_matrix, s_tri_point.reshape(-1, 1))
            # trans_pos += s_center_point[s_init_vertical_axis]
            s_tri_point[0:] = trans_pos.reshape(-1)
            s_tri_point += s_center_point
            

        return s_edge_points
    
    
    