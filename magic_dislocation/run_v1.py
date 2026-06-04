import os
import argparse
import sys
import logging
import numpy as np
from yaml import load, Loader
from ase import Atoms
from magic_dislocation.pipeline import DisplacePipeline, AddDisplacePipeline, DeleteDisplacePipeline
from magic_dislocation.io.ase_io import ase_read, ase_write


def main(configs):
    
    # setting logger 
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    continue_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(continue_formatter)
    
    logger.addHandler(console_handler)
    
    
    # load configs
    pipeline_input_configs = {}
    for k, v in configs.items():
        if type(v) == list:
            v = np.array(v)
        pipeline_input_configs[k] = v
            
    # prepare input config
    input_config = {"filename": pipeline_input_configs['filename'],
                    "format": pipeline_input_configs['format'],
                    "atom_style": pipeline_input_configs['atom_style']
                    }
    
    # read atoms
    atoms = ase_read(**input_config)
    atoms_symbols = atoms.get_chemical_symbols()

    # prepare config for move pipeline
    pipeline_input_configs["positions"] = atoms.get_positions()
    pipeline_input_configs["atom_types"] =  np.array(atoms.get_array("type"))

    pipeline_input_configs["logger"] = logger
    # create pipeline
    if pipeline_input_configs["pipeline_type"] == "displace":
        pipeline = DisplacePipeline(pipeline_input_configs)
    elif pipeline_input_configs["pipeline_type"] == "add_displace":
        pipeline = AddDisplacePipeline(pipeline_input_configs)
    elif pipeline_input_configs["pipeline_type"] == "delete_displace":
        pipeline = DeleteDisplacePipeline(pipeline_input_configs)
    else:
        raise ValueError("The pipeline type is not supported!")
    
    # run the pipeline
    pipeline.run()
    
    # prepare output config
    output_config = {}
    output_config["filename"] = pipeline_input_configs["filename"] + ".moved"
    output_config["format"] = pipeline_input_configs["format"]
    output_config["atom_style"] = pipeline_input_configs["atom_style"]

    # write_results(config, pipeline.results)
    atoms.set_positions(pipeline_input_configs["moved_atoms_positions"])
    if "add" in pipeline_input_configs["pipeline_type"] and "added_atoms_indexes" in pipeline_input_configs:
        added_symbols = [atoms_symbols[i] for i in pipeline_input_configs["added_atoms_indexes"]]
        added_atoms = Atoms(symbols=added_symbols,
                            positions=pipeline_input_configs["added_atoms_positions"])
        atoms += added_atoms
    elif "delete" in pipeline_input_configs["pipeline_type"] and "deleted_atoms_indexes" in pipeline_input_configs:
        del atoms[pipeline_input_configs["deleted_atoms_indexes"]]
    #atoms.center(about=pipeline_input_configs["s_center_point"])
    output_config["images"] = atoms
    ase_write(**output_config)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--yaml_file', type=str, required=True)
    args = parser.parse_args()
    yaml_file = args.yaml_file
    
    configs = load(open(yaml_file, "r", encoding="utf-8").read(), Loader=Loader)  # load configs from the yaml file

    main(configs)
    