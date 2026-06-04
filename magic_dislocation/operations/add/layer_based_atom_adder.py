""" This module contains the LayerBasedAtomAdder class.

This module contains the LayerBasedAtomAdder class, which is used to add atoms copied from other layers to certain positions.

    Typical usage example:
    
    adder = LayerBasedAtomAdder(config)
    adder.run()

"""


import numpy as np

from .base_adder import BaseAtomAdder
from magic_dislocation.utils import get_rotation_info


class LayerBasedAtomAdder(BaseAtomAdder):

    
    def __init__(self, config):
        super().__init__(config)
        self.config = config
        self.layers_for_adding = range(self.config["layers_range_for_adding"][0], self.config["layers_range_for_adding"][1])
        self.added_atoms_offset_vector = self.config["added_atoms_offset_vector"] if "added_atoms_offset_vector" in self.config else None

        
    def create_atoms(self):
        """
        Create atoms based on the atoms from other layers and the shape of S plane
        """
        self.layer_atoms = self.config["layer_info"]["layer_atoms"]
        selected_atoms_indexes = []
        delta_positions = []
        # select the atoms of layers used for adding
        for layer, atoms_indexes in self.layer_atoms.items():
            if layer in self.layers_for_adding:
                selected_atoms_indexes.extend(atoms_indexes)
                if layer == self.layers_for_adding[-1]:
                    delta_positions.extend([[0, 0, 0]]*len(atoms_indexes))
                else:
                    delta_positions.extend([[0, 0, 0]]*len(atoms_indexes))
        delta_positions = np.array(delta_positions)

        selected_atoms_positions = self.config["positions"][selected_atoms_indexes]
        selected_atoms_positions += np.array(delta_positions)
        selected_atoms_types = self.config["atom_types"][selected_atoms_indexes]
        selected_atoms_center_point = np.mean(selected_atoms_positions, axis=0)
            
        # select the atoms to S plane
        if "s_init_direction_vector" not in self.config:
            raise NotImplementedError("The s_init_direction_vector is required!")
        s_init_vertical_axis = self.config["s_init_vertical_axis"]
        s_init_direction_vector = self.config["s_init_direction_vector"]
        s_direction_vector = self.config["s_direction_vector"] if "s_direction_vector" in self.config else s_init_direction_vector
        
        # rotate the selected atoms to the init S plane for easier selection
        layer_direction_vector = self.config["layer_direction_vector"]
        rotate_info = get_rotation_info(layer_direction_vector, s_init_direction_vector)
        if not np.isnan(rotate_info).any():
            # centeralize the selected atoms
            temp_selected_atoms_positions = selected_atoms_positions - selected_atoms_center_point
            temp_selected_atoms_positions = np.dot(temp_selected_atoms_positions, rotate_info)
            # move back to the original position
            temp_selected_atoms_positions += selected_atoms_center_point
        else:
            temp_selected_atoms_positions = selected_atoms_positions.copy()
        
        new_indexes = []
        if self.config["s_type"] == "rectangle":
            count_indexes = [0, 1, 2]
            count_indexes.remove(count_indexes[s_init_vertical_axis])
            for i, atom_position in enumerate(temp_selected_atoms_positions):
                if atom_position[count_indexes[0]] < self.config["s_center_point"][count_indexes[0]] + self.config["s_length"]/2 and \
                    atom_position[count_indexes[0]] > self.config["s_center_point"][count_indexes[0]] - self.config["s_length"]/2 and \
                    atom_position[count_indexes[1]] < self.config["s_center_point"][count_indexes[1]] + self.config["s_width"]/2 and \
                    atom_position[count_indexes[1]] > self.config["s_center_point"][count_indexes[1]] - self.config["s_width"]/2:
                    new_indexes.append(i)
                    
        elif self.config["s_type"] == "loop":
            S_R = self.config["s_radius"] * self.config["lattice"]
            for i, atom_position in enumerate(temp_selected_atoms_positions):
                delta = atom_position - selected_atoms_center_point
                # delta[s_init_vertical_axis] = 0
                if np.linalg.norm(delta) < S_R:
                    new_indexes.append(i)
        else:
            new_indexes = range(len(selected_atoms_positions))

        selected_atoms_indexes = np.array(selected_atoms_indexes)[new_indexes]
        selected_atoms_positions = selected_atoms_positions[new_indexes]
        selected_atoms_types = selected_atoms_types[new_indexes]
        selected_atoms_center_point = np.mean(selected_atoms_positions, axis=0)

        if "resize_factor" in self.config:
            selected_atoms_positions = selected_atoms_positions - selected_atoms_center_point
            selected_atoms_positions *= np.array(self.config["resize_factor"])
            selected_atoms_positions = selected_atoms_positions + selected_atoms_center_point
            selected_atoms_center_point = np.mean(selected_atoms_positions, axis=0)        
        
        # move to the position of the S plane
        if self.added_atoms_offset_vector is None:
            self.added_atoms_offset_vector = self.config["s_center_point"] - selected_atoms_center_point
            print("The added atoms offset vector is: ", self.added_atoms_offset_vector)
        else:
            print("The added atoms offset vector is: ", self.added_atoms_offset_vector)
            
        selected_atoms_positions += self.added_atoms_offset_vector
            
        # rotate the added atoms
        rotate_info = get_rotation_info(layer_direction_vector, s_direction_vector)

        if not np.isnan(rotate_info).any():
            # centeralize the selected atoms
            selected_atoms_positions -= self.config["s_center_point"]
            selected_atoms_positions = np.dot(selected_atoms_positions, rotate_info)
            # move back to the original position
            selected_atoms_positions += self.config["s_center_point"]
        else:           
            selected_atoms_positions = selected_atoms_positions.copy()
            
        added_atoms_indexes = selected_atoms_indexes
        added_atoms_positions = selected_atoms_positions
        added_atoms_types = selected_atoms_types
            
        return added_atoms_indexes, added_atoms_positions, added_atoms_types
        

    def run(self):
        added_atoms_indexes, added_atoms_positions, added_atoms_types = self.create_atoms()
        result = dict()
        result["added_atoms_indexes"] = added_atoms_indexes
        result["added_atoms_positions"] = added_atoms_positions
        result["added_atoms_types"] = added_atoms_types
        return result