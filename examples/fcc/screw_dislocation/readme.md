[Displace-Pipeline]

In this directory, we plan to create a line screw dislocation 1/2<110> on a FCC system, whose crystal direction is X ：0 0 1, Y : 1 1 0, Z : -1 1 0. The dislocation line is still parallel to the Z-axis and so the burgers vector is also parallel to Z-axis.

The direction of burgers vector is parallel to Z-axis so we should move atoms along Z-axis. The norm of burgers vector is sqrt(2)/2 = 0.707. Therefore, the final input Burgers Vector (Cartesian) for this system is [0, 0, 0.707].

The layerization direction is usually perpendicular to the direction of burguers vector. Here, we use the Y-axis [0,1,0] to serve as the layerization direction.

The initial S plane is perpendicular to the Y-axis so the initial direction is Y.

To obtain a line-shape dislocation, we fisrt need to define a rectangle S plane. However, the rectangle only has an edge in the system. Other three edges are our of the system. To achieve this requirement, we set the rectangle's length and width to 140.54 (The whole range of system along Z-axis) and 1000 (far larger than the system's range along Y-axis).


We also provide a new_config.yaml containing parameter settings for command-line runing method.
All related parameters can be found in interface_screw.png and new_config.yaml. Users can run them via the following two ways:

```
bash scripts/run_based_ui.sh
```



or

```
cd magic_dislocation
python run.py \
    --yaml_file '../examples/fcc/screw_dislocation/new_config.yaml'
```