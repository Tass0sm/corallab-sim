import numpy as np

from scipy.spatial.transform import Rotation as R


def get_rotation(rotq=None, euler=None, rotvec=None, t_matrix=None):
    """ utility function to create transformation matrix from different input forms """
    if rotq is not None:
        m = R.from_quat(rotq)
    elif euler is not None:
        m = R.from_euler('xyz', euler)
    elif rotvec is not None:
        m = R.from_rotvec(rotvec)
    elif t_matrix is not None:
        m = R.from_matrix(t_matrix[:-1, :-1])

    return m


def get_transform(rotq=None, euler=None, rotvec=None, matrix=None, pos=(0, 0, 0)):
    """ utility function to create transformation matrix from different input forms """
    trans = np.eye(4)

    if rotq is not None:
        trans[:-1, :-1] = R.from_quat(rotq).as_matrix()
    elif euler is not None:
        trans[:-1, :-1] = R.from_euler('xyz', euler).as_matrix()
    elif rotvec is not None:
        trans[:-1, :-1] = R.from_rotvec(rotvec).as_matrix()
    elif matrix is not None:
        trans[:-1, :-1] = matrix

    trans[:-1, -1:] = np.array(pos).reshape(-1, 1)

    return trans


def invert_transform(transform):
    return np.linalg.inv(transform)


def transform_point(transform, point):
    homogenous_point = np.array([*point, 1])
    homogenous_point_prime = np.matmul(transform, homogenous_point)
    point_prime = homogenous_point_prime[0:3] / homogenous_point_prime[3]
    return point_prime


def compute_transform(a_points, b_points):
    """
    - a_points: N x 3 matrix of points p1, p2, ... pn expressed in space A
    - b_points: N x 3 matrix of points p1, p2, ... pn expressed in space B

    returns T mapping points from space A to space B

    https://math.stackexchange.com/questions/1519134/how-to-find-the-best-fit-transformation-between-two-sets-of-3d-observations#1519503
    """
    a_cen = a_points.mean(axis=0)
    b_cen = b_points.mean(axis=0)

    P = a_points.T @ a_points - np.outer(a_cen, a_cen)
    Q = b_points.T @ a_points - np.outer(b_cen, a_cen)

    # # transformation which subtracts a_cen
    # a_reset_t = np.array([
    # T_a_to_b = Q @ np.linalg.pinv(P)

    return Q, np.linalg.pinv(P), a_cen, b_cen


def apply_transform(tr: tuple, src: np.ndarray) -> np.ndarray:
    Q, Pinv, s_cen, d_cen = tr
    return (Q @ Pinv @ (src - s_cen).T).T + d_cen


def change_basis():
    pass


def change_basis():
    pass
