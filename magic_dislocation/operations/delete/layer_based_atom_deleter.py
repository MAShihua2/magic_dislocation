""" This module contains the LayerBasedSelector class.

This module contains the LayerBasedSelector class, which is used to select atoms based on the layer.

    Typical usage example:
    
    deleter = LayerBasedAtomDeleter(config)
    deleter.run()

"""


import numpy as np

from .base_deleter import BaseAtomDeleter
from magic_dislocation.utils import get_rotation_info


class LayerBasedAtomDeleter(BaseAtomDeleter):
    
    def __init__(self, config):
        super().__init__(config)
        self.config = config
        self.layer_direction_vector = self.config["layer_direction_vector"]
        self.s_center_point = self.config["s_center_point"]
        
        
    def calculate_range_to_delete(self):

        layer_direction_vector = self.layer_direction_vector
        s_center_point = self.s_center_point
        
        range_to_delete = np.linalg.norm(self.config["burgers_vector_fraction"] * self.config["burgers_vector_direction"]) * self.config["lattice"]
        normalzied_layer_direction_vector = layer_direction_vector / np.linalg.norm(layer_direction_vector)
        A_point = s_center_point + normalzied_layer_direction_vector * range_to_delete/2
        B_point = s_center_point - normalzied_layer_direction_vector * range_to_delete/2
        
        range_positions = np.array([A_point, B_point])
        return range_positions
    
    
    def select_atoms_based_on_layer(self):
        layer_direction_vector = self.layer_direction_vector
        range_positions = self.calculate_range_to_delete()
        
        # get range points' projection on the s direction vector
        delta_vector = range_positions - self.config["layer_direction_vector"]
        range_projection = np.dot(delta_vector, layer_direction_vector) / np.linalg.norm(layer_direction_vector)
        range_projection = np.round(range_projection, 0)
        range_projection = np.array([min(range_projection), max(range_projection)])

        # get the layer indexes
        layer_projections = self.config["layer_info"]["layer_projection"]
        selected_atoms_indexes = []
        selected_atoms_positions = []
        unselected_atoms_positions = []
        for i, projection in enumerate(layer_projections):
            if projection >= range_projection[0] and projection <= range_projection[1]:
                selected_atoms_indexes.append(i)
                selected_atoms_positions.append(self.config["positions"][i])
            else:
                unselected_atoms_positions.append(self.config["positions"][i])
                
        return {"selected_atoms_indexes": selected_atoms_indexes,
                "selected_atoms_positions": np.array(selected_atoms_positions),
                "unselected_atoms_positions": np.array(unselected_atoms_positions)}
        

    def select_atoms_based_on_S_plane(self, selected_atoms_based_on_layer):
        """
        Select atoms based on the S plane.
        """
        selected_atoms_indexes = selected_atoms_based_on_layer["selected_atoms_indexes"]
        selected_atoms_positions = selected_atoms_based_on_layer["selected_atoms_positions"]
        selected_atoms_center_point = np.mean(selected_atoms_positions, axis=0)

        # select the atoms based on the S plane
        ## get parameters
        if "s_init_direction_vector" not in self.config:
            raise NotImplementedError("The s_init_direction_vector is required!")
        s_init_vertical_axis = self.config["s_init_vertical_axis"]
        s_init_direction_vector = self.config["s_init_direction_vector"]
        layer_direction_vector = self.layer_direction_vector
        ## rotate the selected atoms to the init S plane for easier selection
        
        rotate_info = get_rotation_info(layer_direction_vector, s_init_direction_vector)
        if not np.isnan(rotate_info).any():
            # centeralize the selected atoms
            temp_selected_atoms_positions = selected_atoms_positions - selected_atoms_center_point
            temp_selected_atoms_positions = np.dot(temp_selected_atoms_positions, rotate_info)
            # move back to the original position
            temp_selected_atoms_positions += selected_atoms_center_point
        else:
            temp_selected_atoms_positions = selected_atoms_positions.copy()
        
        ## select according to the S plane shape
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
            print("The S_R is: ", S_R)
            for i, atom_position in enumerate(temp_selected_atoms_positions):
                delta = atom_position - selected_atoms_center_point
                # delta[s_init_vertical_axis] = 0
                if np.linalg.norm(delta) < S_R:
                    new_indexes.append(i)
                    
            print(len(new_indexes))
        
        else:
            new_indexes = range(len(selected_atoms_positions))

        new_selected_atoms_indexes = []
        new_selected_atoms_positions = []
        new_unselected_atoms_positions = []
        for i, atom_position in enumerate(selected_atoms_based_on_layer["selected_atoms_positions"]):
            if i in new_indexes:
                new_selected_atoms_indexes.append(selected_atoms_indexes[i])
                new_selected_atoms_positions.append(atom_position)
            else:
                new_unselected_atoms_positions.append(atom_position)
        
        new_selected_atoms_indexes = np.array(new_selected_atoms_indexes)
        new_selected_atoms_positions = np.array(new_selected_atoms_positions)
        new_unselected_atoms_positions = np.array(new_unselected_atoms_positions)
        
        return {"selected_atoms_indexes": new_selected_atoms_indexes,
                "selected_atoms_positions": new_selected_atoms_positions,
                "unselected_atoms_positions": new_unselected_atoms_positions}
        
    
     
    def select_atoms(self):
        """
        Select atoms based on the layer.
        """
        self.layer_atoms = self.config["layer_info"]["layer_atoms"]
        
        # select the atoms based on the layer
        selected_atoms_based_on_layer = self.select_atoms_based_on_layer()

        selected_atoms_based_on_s_plane = self.select_atoms_based_on_S_plane(selected_atoms_based_on_layer)
        
        selected_atoms_indexes = selected_atoms_based_on_s_plane["selected_atoms_indexes"]
        selected_atoms_positions = selected_atoms_based_on_s_plane["selected_atoms_positions"]
        unselected_atoms_positions = selected_atoms_based_on_layer["unselected_atoms_positions"].tolist()  + \
                                    selected_atoms_based_on_s_plane["unselected_atoms_positions"].tolist()
        
        unselected_atoms_positions = np.array(unselected_atoms_positions)
        
        results = { "selected_atoms_indexes": selected_atoms_indexes,
                    "selected_atoms_positions": selected_atoms_positions,
                    "unselected_atoms_positions": unselected_atoms_positions
                   }
            
        return results
        

    def run(self):
        results = self.select_atoms()
        return results