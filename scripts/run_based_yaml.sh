# CUR_DIR=$(cd $(dirname $0); pwd)
# cd $CUR_DIR
cd magic_dislocation

############################ FCC #######################################

# fcc edge dislocation
# python run.py \
#     --yaml_file '../examples/fcc/edge_dislocation/new_config.yaml'

# fcc screw dislocation
# python run.py \
#     --yaml_file '../examples/fcc/screw_dislocation/new_config.yaml'


# fcc partial dislocation loop
# python run.py \
#     --yaml_file '../examples/fcc/partial_dislocation_loop/new_config.yaml'


# fcc rotate loop
# python run.py \
#     --yaml_file '../examples/fcc/rotation_loop/new_config.yaml'



# fcc shape sin line
python run.py \
    --yaml_file '../examples/fcc/shape_sin_line/new_config.yaml'


############################ BCC #######################################
# b
# python run.py \
#     --yaml_file '../examples/bcc/100_habit_plane/new_config.yaml'

# 110 habit plane
# python run.py \
#     --yaml_file '../examples/bcc/110_habit_plane/new_config.yaml'


############################ Cubic #######################################
# python run.py \
#     --yaml_file '../examples/z cubic/SrTiO3/new_config.yaml'
