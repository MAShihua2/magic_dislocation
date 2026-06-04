import numpy as np
from scipy.spatial.transform import Rotation as R

def get_rotation_matric_scipy(n1, n2):
    n1 = n1 / np.linalg.norm(n1)
    n2 = n2 / np.linalg.norm(n2)
    rotation_matrix = R.align_vectors([n2], [n1])[0].as_matrix()
    return rotation_matrix

def get_rotation_info(insert_plane, target_plane):
    # define rotation axis
    rotation_axis = np.cross(insert_plane, target_plane)
    rotation_axis = np.sqrt(rotation_axis * rotation_axis / sum(rotation_axis * rotation_axis))
    u_x = rotation_axis[0]
    u_y = rotation_axis[1]
    u_z = rotation_axis[2]
    if isinstance(insert_plane, list):
        insert_plane = np.array(insert_plane)
    if isinstance(target_plane, list):
        target_plane = np.array(target_plane)
    cos_theta = insert_plane.dot(target_plane) / np.sqrt(sum(insert_plane * insert_plane) * sum(target_plane * target_plane))
    # define rotation theta
    sin_theta = np.sqrt(1 - cos_theta * cos_theta)
    rotation_matrix = np.array([[cos_theta + u_x * u_x * (1 - cos_theta), u_x * u_y * (1 - cos_theta) - u_z * sin_theta,
                                 u_x * u_z * (1 - cos_theta) + u_y * sin_theta],
                                [u_y * u_x * (1 - cos_theta) + u_z * sin_theta, cos_theta + u_y * u_y * (1 - cos_theta),
                                 u_y * u_z * (1 - cos_theta) - u_x * sin_theta],
                                [u_z * u_x * (1 - cos_theta) - u_y * sin_theta,
                                 u_z * u_y * (1 - cos_theta) + u_x * sin_theta,
                                 cos_theta + u_z * u_z * (1 - cos_theta)]
                                ])
    # print("Custom rotation matrix calculation:")
    # print(rotation_matrix)
    print("Using scipy to calculate rotation matrix:")
    rotation_matrix = get_rotation_matric_scipy(insert_plane, target_plane)
    return rotation_matrix