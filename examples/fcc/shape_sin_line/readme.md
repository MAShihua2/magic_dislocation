[Displace-Pipeline]

In this directory, we plan to create a sin line dislocation 1/2<110> on a FCC system, whose crystal direction is X ：0 0 1, Y : 1 1 0, Z : -1 1 0.

The direction of burgers vector is parallel to Y-axis so we should move atoms along Y-axis. The norm of burgers vector is sqrt(2)/2 = 0.707. Therefore, the final input Burgers Vector (Cartesian) for this system is [0, 0.707, 0].

The layerization direction is usually perpendicular to the direction of burguers vector. Here, we use the X-axis [1,0,0] to serve as the layerization direction.

The initial S plane is perpendicular to the X-axis so the initial direction is X.

To obtain a sin line-shape dislocation, we fisrt need to define a rectangle S plane. However, the rectangle only has an edge in the system. Other three edges are our of the system. To achieve this requirement, we set the rectangle's length and width to 140.54 (The whole range of system along Z-axis) and 200 (far larger than the system's range along Y-axis). Then, we need to define the parameters of sin function line, including:
- A
- Omega
- Start Point
- End Point

A and Omega determine the concrete shape of sin function line. Start Point and End Point determine the concrete position of the line (which axis the line is parallel to).


All related parameters can be found in interface_partial_dislocation.png and new_config.yaml. Users can run them via the following two ways:

```
bash scripts/run_based_ui.sh
```



or

```
cd magic_dislocation
python run.py \
    --yaml_file '../examples/fcc/shape_sin_line/new_config.yaml'
```