""" A base module for moving atoms based on solid angle

In this module, we define a base module for moving atoms based on solid angle, containing necessay configs,

"""

import numpy as np
from .base_mover import BaseMover


class SolidAngleMover(BaseMover):

    def __init__(self, config):
        super().__init__(config)
        if "move_direction_vector" in self.config:
            self.move_direction_vector = self.config["move_direction_vector"] if type(self.config["move_direction_vector"]) == np.ndarray \
                else np.array(self.config["move_direction_vector"])
            self.move_direction_vector = self.move_direction_vector * self.config["move_step"]
        elif "burgers_vector" in self.config:       
            self.move_direction_vector = self.config["burgers_vector"] if type(self.config["burgers_vector"]) == np.ndarray \
                else np.array(self.config["burgers_vector"])
        else:
            raise ValueError("The move direction vector is not provided!")
        self.positions = self.config["positions"]
        self.logger = self.config.get("logger", None)
        
        
    def calculate_solid_angle(self, u1, u2, u3):
        """
        Calculate the solid angle for each atom.
        """
        # u1: n * 3
        eps = 1e-12
        denominator = 1 + (u2 * u3).sum(1) + (u1 * u3).sum(1) + (u1 * u2).sum(1)
        numerator = (np.cross(u2, u3) * u1).sum(1)
        s_tri = np.arctan(numerator / denominator)

        mask_neg_denominator = np.where(denominator < 0, 1, 0)
        mask_neg_numerator = np.where(numerator < 0, -np.pi, np.pi)
        delta = mask_neg_denominator * mask_neg_numerator
        s_tri += delta

        eps_denominator_mask = np.where(abs(denominator) < eps, 1, 0)
        eps_numerator_mask = np.where(abs(numerator) < eps, 1, 0)
        eps_mask = eps_denominator_mask * eps_numerator_mask
        s_tri = s_tri * (1 - eps_mask)
        eps_delta = eps_mask * 0.5 * np.pi
        s_tri += eps_delta
        return 2 * s_tri
    
    
    def calculate_move_distance(self, target_atoms, vertex_points, move_direction_vector):
        """
        Calculate the move distance for each atom.
        """
        
        def define_S(s_center, edge_points):
            """
            s_center: the center point of S S plane
            edge_points: the vertex points of S planee
            """
            s_tri_points = [[s_center, edge_points[i], edge_points[(i+1)%len(edge_points)]] for i in range(len(edge_points))]
            return np.array(s_tri_points)
        
        s_tri_points = define_S(self.config["s_center_point"], vertex_points)
        
        moved_atoms = []

        move_b = self.config["lattice"] * self.move_direction_vector
        self.logger.info(f"move_b is: {move_b}")
        for i, target_atom in enumerate(target_atoms):
            di_vectors = s_tri_points[:, :, :] - target_atom
            di_vectors = di_vectors / np.sqrt((di_vectors * di_vectors).sum(2)).reshape(s_tri_points.shape[0], 3, 1)
            u1 = di_vectors[:, 0, :]
            u2 = di_vectors[:, 1, :]
            u3 = di_vectors[:, 2, :]
            solid_angles = self.calculate_solid_angle(u1, u2, u3)
            s = sum(solid_angles)
            us = -s * move_b / (4 * np.pi)
            moved_atom = target_atom + us
            moved_atoms.append(moved_atom)
        
        moved_atoms = np.array(moved_atoms)
        
        return moved_atoms
        

    def move(self):
        """
        Move atoms based on the solid angle.
        """
        selected_atoms_indexes = self.config.get("selected_atoms_indexes", None)
        if selected_atoms_indexes is not None:
            self.target_positions = self.positions[selected_atoms_indexes]
        else:
            self.target_positions = self.positions
            
        self.vertex_points = self.config["vertex_points"]
        moved_atoms = self.calculate_move_distance(self.target_positions, self.vertex_points, self.move_direction_vector)
        
        result = {"moved_target_atoms_positions": moved_atoms}
        
        return result
        
        