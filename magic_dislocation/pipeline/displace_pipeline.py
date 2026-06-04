""" Move pipeline module for moving atoms.

In this module, we define a class for moving atoms, containing necessary configs,
functions for moving atoms.

  Typical usage example:

  pipeline = MovePipeline(config)
  pipeline.run()
"""


from magic_dislocation.pipeline.base_pipeline import BasePipeline
from magic_dislocation.operations.define_s import DefineRectangleS, DefineSinS, DefineLoopS
from magic_dislocation.operations.layerize.vector_based_layerizer import VectorBasedLayerizer
from magic_dislocation.operations.select.layer_based_selector import LayerBasedSelector
from magic_dislocation.operations.move.solid_angle_mover import SolidAngleMover
from magic_dislocation.visualization.atoms_visualizer import Visualizer


class DisplacePipeline(BasePipeline):
    """
    A class for moving atoms.
    """

    def __init__(self, config):
        super().__init__(config)
        # self.config = config
        self.logger = config.get("logger", None)
        self.init_submodules()
        
    def init_submodules(self):
        """
        Initialize the submodules.
        """
        
        if self.config["s_type"] == "rectangle":
            self.define_s = DefineRectangleS(self.config)
        elif self.config["s_type"] == "sin":
            self.define_s = DefineSinS(self.config)
        elif self.config["s_type"] == "loop":
            self.define_s = DefineLoopS(self.config)
        else:
            raise ValueError("The S type is not supported!")
        
        
        self.layerizer = VectorBasedLayerizer(self.config)
        
        self.atom_selector = LayerBasedSelector(self.config)
        
        self.atom_mover = SolidAngleMover(self.config)
            
        self.visualizer = Visualizer(self.config)
        

    def layerize(self):
        """
        Layerize atoms.
        """
        results = self.layerizer.run()
        
        if self.config["visualize_layer"]:
            vis_input = dict()
            vis_input["layer_atoms"] = {key: self.config["positions"][value] for key, value in results["layer_info"]["layer_atoms"].items()}
            self.visualizer.show(vis_input["layer_atoms"])
        
        layer_num = len(results["layer_info"]["layer_atoms"])
        self.logger.info(f"The number of layers is: {layer_num}")
        
        self.config["layer_info"] = results["layer_info"]
        
        return results
        
        
    def define_s_plane(self):
        """
        Define the S plane.
        """
        results = self.define_s.run()
        self.config["vertex_points"] = results["vertex_points"] if "vertex_points" in results else results["rotated_vertex_points"]

        if self.config["visualize_s"]:
            self.visualizer.show(results, plot_type="line")
        
        return results
    
    
    def select_atoms(self):
        """
        Select atoms.
        """
        results = self.atom_selector.run()
        vis_input = dict()
        vis_input["selected_atoms_positions"] = self.config["positions"][results["selected_atoms_indexes"]]
        self.config["selected_atoms_indexes"] = results["selected_atoms_indexes"]
        
        if self.config["visualize_select"]:
            self.visualizer.show(vis_input)
        
        return results
        

    def move_atoms(self,):
        """
        Move atoms to the specified position.

        Args:
            positions: The positions of the atoms.
        """
        results = self.atom_mover.run()
        vis_input = dict()
        vis_input["target_atoms_positions"] = self.config["positions"][self.config["selected_atoms_indexes"]]
        vis_input["moved_target_atoms_positions"] = results["moved_target_atoms_positions"]
        
        
        if self.config["visualize_move"]:
            self.visualizer.show(vis_input)
            
        self.config["moved_atoms_positions"] = self.config["positions"].copy()
        self.config["moved_atoms_positions"][self.config["selected_atoms_indexes"]] = results["moved_target_atoms_positions"]
        
        return results


    def run(self):
        self.layerize()
        self.logger.info("Layerize atoms successfully!")
        self.define_s_plane()
        self.logger.info("Define S plane successfully!")
        self.select_atoms()
        self.logger.info("Select atoms successfully!")
        self.move_atoms()
        self.logger.info("Move atoms successfully!")