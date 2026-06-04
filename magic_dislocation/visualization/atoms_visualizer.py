""" This is a 3D visualizer for the atoms in the system.

This module is used to visualize the atoms in the system in 3D.
    
        Typical usage example:
    
        visualizer = Visualizer(atoms)
        visualizer.show()
"""

import numpy as np
from matplotlib import pyplot as plt

class Visualizer:
    """
    A class for visualizing atoms in 3D.
    """
    
    def __init__(self, config):
        pass
    
        
    def show(self, atoms_dict, plot_type="scatter"):
        """
        Show the atoms in 3D.
        """
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        
        for key in atoms_dict.keys():
            atoms = atoms_dict[key]
            if len(atoms.reshape(-1)) == 3:
                reshape_atoms = atoms.reshape(-1)
                ax.scatter(reshape_atoms[0], reshape_atoms[1], reshape_atoms[2], label=key, s=5)
            else:
                if plot_type == "scatter":
                    ax.scatter(atoms[:, 0], atoms[:, 1], atoms[:, 2], label=key, s=5)
                elif plot_type == "line":
                    new_atoms = list(atoms.copy()) + [atoms[0]]
                    new_atoms = np.array(new_atoms)
                    ax.plot(new_atoms[:, 0], new_atoms[:, 1], new_atoms[:, 2], label=key)
        ax.set_xlabel('X-axis')
        ax.set_ylabel('Y-axis')
        ax.set_zlabel('Z-axis')
        plt.legend()
        plt.show()
