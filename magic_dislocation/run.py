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
    """
    config
    
    """
    # setting logger 
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    continue_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(continue_formatter)
    
    logger.addHandler(console_handler)
    
    
    # load configs
    pipeline_configs = configs['pipeline']
    data_config = configs['data']
    layerization_config = configs['layerization']
    s_plane_config = configs['s_plane']
    move_config = configs['moving']
    
    logger.info("Pipeline config: {}".format(pipeline_configs))
    logger.info("Data config: {}".format(data_config))
    logger.info("Layerization config: {}".format(layerization_config))
    logger.info("S plane config: {}".format(s_plane_config))
    logger.info("Move config: {}".format(move_config))
    
    # prepare input config
    input_config = {"filename": data_config['filename'],
                    "format": data_config['format'],
                    "atom_style": data_config['atom_style']
                    }
    
    # read atoms
    atoms = ase_read(**input_config)
    atoms_symbols = atoms.get_chemical_symbols()

    # prepare config for move pipeline
    pipeline_input_configs = {"positions": atoms.get_positions(),
                              "atom_types": np.array(atoms.get_array("type"))}
    for k, v in configs.items():
        for kk, vv in v.items():
            if type(vv) == list:
                vv = np.array(vv)
            pipeline_input_configs[kk] = vv
    
    pipeline_input_configs["logger"] = logger
    
    # create pipeline
    if pipeline_configs["pipeline_type"] == "displace":
        pipeline = DisplacePipeline(pipeline_input_configs)
    elif pipeline_configs["pipeline_type"] == "add_displace":
        pipeline = AddDisplacePipeline(pipeline_input_configs)
    elif pipeline_configs["pipeline_type"] == "delete_displace":
        pipeline = DeleteDisplacePipeline(pipeline_input_configs)
    else:
        raise ValueError("The pipeline type is not supported!")
    
    # run the pipeline
    pipeline.run()
    
    # prepare output config
    output_config = {}
    output_config["filename"] = data_config["filename"] + ".moved"
    output_config["format"] = data_config["format"]
    output_config["atom_style"] = data_config["atom_style"]

    # write_results(config, pipeline.results)
    atoms.set_positions(pipeline_input_configs["moved_atoms_positions"])
    if "add" in pipeline_configs["pipeline_type"] and "added_atoms_indexes" in pipeline_input_configs:
        added_symbols = [atoms_symbols[i] for i in pipeline_input_configs["added_atoms_indexes"]]
        added_atoms = Atoms(symbols=added_symbols,
                            positions=pipeline_input_configs["added_atoms_positions"])
        atoms += added_atoms
    elif "delete" in pipeline_configs["pipeline_type"] and "deleted_atoms_indexes" in pipeline_input_configs:
        del atoms[pipeline_input_configs["deleted_atoms_indexes"]]
    # atoms.center(about=s_plane_config["s_center_point"])
    output_config["images"] = atoms
    ase_write(**output_config)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--yaml_file', type=str, required=True)
    args = parser.parse_args()
    yaml_file = args.yaml_file
    
    configs = load(open(yaml_file, "r", encoding="utf-8").read(), Loader=Loader)  # load configs from the yaml file

    main(configs)
    