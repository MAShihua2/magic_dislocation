[Move-Pipeline]

In this directory, we plan to create a slanted loop dislocation 1/6<112> on a FCC system, whose crystal direction is X ：-1 1 0, Y : 1 1 1, Z : 1 1 -2.

The direction of burgers vector is parallel to Y-axis so we should move atoms along Y-axis. The norm of burgers vector is sqrt(6)/6 = 0.408. Therefore, the final input Burgers Vector (Cartesian) for this system is [0, 0.408, 0].

The layerization direction is usually perpendicular to the direction of burguers vector. Here, we use the Z-axis [0,0,1] to serve as the layerization direction.

The initial S plane is perpendicular to the Z-axis so the initial direction is Z.

Then, we want to rotate the S plane to the 112 direction so we convert the 112 direction into cartesian coordinate and then obtain the rotated direction is [0, 1, 2.8286].

All related parameters can be found in interface_partial_dislocation.png and new_config.yaml. Users can run them via the following two ways:

```
bash scripts/run_based_ui.sh
```



or

```
cd magic_dislocation
python run.py \
    --yaml_file '../examples/fcc/rotation_loop/new_config.yaml'
```