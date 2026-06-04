[Displace-Pipeline]

To more clearly demonstrate how to construct an edge dislocation line $1/2<110>$ in an FCC system (the crystal direction is $X:0 0 1, Y:1 1 0, Z:-1 1 0$) using MagicDislocation, we provide the parameters to build the edge dislocation using the GUI method, as shown in the figure interface_edge.png. Generally, the construction of the edge dislocation needs to remove some atoms. In this case, we have deleted the target atoms in the data file, so we just need to move atoms and use the dispace pipeline. This setting can satisfy users who want to delete or add atoms manually. The dislocation line is based on a rectangle S plane, so we choose Rectangle in the left column cards.

For data related parameters, we should provide the path of data file, data file type, lattice, data structure, and other parameters accepted by the ASE IO module (Kwargs box).

For the layerization direction, it can be perpendicular to the direction of the Burgers vector or consistent with the direction of the S plane. Here, we let it be consistent with the direction of the S plane, which is perpendicular to the X-axis. So, the layerization direction is $(1, 0, 0)$.

For the S plane, we need to provide its center position, the initial direction, which is perpendicular to the coordinate axis. The initial direction satisfies the requirements for the S planes perpendicular to the coordinate axis. For an S plane not perpendicular to the coordinate axis, we should assign its direction via the rotated direction parameter. MagicDislocation will create an initial S plane whose direction is the initial direction and rotate the initial S plane to obtain the final S plane whose direction is the rotated direction.

For rectangle setting, to obtain a dislocation line, we first define a rectangle S plane. The rectangle only has an edge in the system. The other three edges are out of the system. To achieve this requirement, we set the rectangle's length and width to 181.5 (larger than the system range along the Z-axis) and 400 (far larger than the system's range along the Y-axis), respectively. These two values could be adjusted by users.

For displacement setting, the layer range is used to select atoms need to be moved. Only atoms whose layer ids are in the layer range will be moved. The "optional" means that all atoms should be moved. The burgers vector (cartesian) input requires the displacement vector converted by the Burgers vector. In this case, the direction of the Burgers vector is parallel to the Y-axis, so we should move the atoms along the Y-axis. The norm of the Burgers vector is $\sqrt2/2$. Therefore, the final input Burgers Vector (Cartesian) for this system is $(0, 0.707, 0)$.

For visualization, we can determine which stages will be visualized in the process of constructing dislocation by selecting the boxes before the stages.


Besides, we also provide a new_config.yaml containing parameter settings for command-line runing method.
All related parameters can be found in interface_edge.png and new_config.yaml. Users can run them via the following two ways:

```
bash scripts/run_based_ui.sh
```



or

```
cd magic_dislocation
python run.py \
    --yaml_file '../examples/fcc/edge_dislocation/new_config.yaml'
```