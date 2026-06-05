"""Test pipeline module.

In this module, we will test the functions in io module with multiple cases.

Typical usage example:
"""

# import os
# import sys

import numpy as np

# sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from magic_dislocation.pipeline.displace_pipeline import DisplacePipeline
from magic_dislocation.io.ase_io import ase_read, ase_write

import logging
# setting logger 

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
    
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
continue_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(continue_formatter)
    
logger.addHandler(console_handler)    

class BasePipelineTester:
    def __init__(self):
        pass

    def test_run(self):
        pass
    
    
class DisplacePipelineTester(BasePipelineTester):
    
    def __init__(self, config):
        self.config = config
        
    def test_run(self):
        """
        Test the run operation.
        """
        pipeline = DisplacePipeline(self.config)
        pipeline.run()

config = {}
file_name = r'../examples/fcc/partial_dislocation_loop/Ni.data'
config = {"filename": file_name,
          "format": "lammps-data",
          "atom_style": "atomic",
          }

atoms = ase_read(**config)
cells = atoms.get_cell()
center_mass = atoms.get_center_of_mass()

print(cells)
print(center_mass)

print(cells.complete())

# exit()
config["positions"] = atoms.get_positions()
config["logger"] = logger
# parameters for define_s
config["s_center_point"] = np.array([0.6, 1, 0.36])
config["s_type"] = "rectangle"
config["s_length"] = 40
config["s_width"] = 40
config["s_init_vertical_axis"] = 2 # 0: x, 1: y, 2: z
config["s_direction_vector"] = None
config["visualize_s"] = False
config["visualize_layer"] = False
config["visualize_select"] = False
config["visualize_move"] = False
config["layer_direction_vector"] = [0, 0, 1]
config["move_direction_vector"] = [0, 1, 0]
config["lattice"] = 3.556
config["move_step"] = 0.408

tester = DisplacePipelineTester(config)
tester.test_run()

output_file = r'../examples/fcc/partial_dislocation_loop/Ni.data.moved'
write_config = {}
write_config["format"] = "lammps-data"
write_config["atom_style"] = "atomic"
write_config["filename"] = output_file
write_config["masses"] = True
write_config["velocities"] = True
atoms.set_positions(config["moved_atoms_positions"])
atoms.set_center_of_mass(center_mass)
write_config["images"] = atoms

ase_write(**write_config)
