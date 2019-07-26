import pyproj
import numpy as np
from .coords import ECEF, LLA
import scipy.spatial


def get_axis(lat0, lon0, alt0, lat1, lon1, alt1):
    v0 = pyproj.transform(LLA, ECEF, lon0, lat0, alt0, radians=False)
    v1 = pyproj.transform(LLA, ECEF, lon1, lat1, alt1, radians=False)
    v = np.array(v1) - np.array(v0)
    return v / np.linalg.norm(v)


def rotate(north, south, west, east, vertices):
    x = get_axis(south, east, 0., south, west, 0.)
    y = get_axis((north + south) / 2, (east + west) / 2, 0.,
                 (north + south) / 2, (east + west) / 2, 1000.)
    r, _ = scipy.spatial.transform.Rotation.match_vectors(
        [[1., 0., 0.], [0., 1., 0.]], [x, y])
    return r.apply(vertices)


def center(vertices):
    x, _, z = np.mean(vertices, axis=0)
    _, y, _ = vertices.min(axis=0)
    return np.subtract(vertices, [x, y, z])


def scale(vertices, factor):
    return vertices * factor * 1000


def fill(vertices, faces, rows, cols, depth):

    # this is mostly hacky garbage that only really makes sense for an stl file, might not be the best for a general mesh

    vertices = vertices + np.array([0., depth, 0.])

    base_verts = []
    base_faces = []

    for i in range(rows):
        base_verts.append([vertices[i * cols][0], 0, vertices[i * cols][2]])

    for i in range(1, rows):
        base_faces.append((cols * (i - 1), len(vertices) + (i - 1), cols * i))
        base_faces.append(
            (cols * i, len(vertices) + (i - 1), len(vertices) + i))

    for i in range(rows):
        base_verts.append([vertices[i * cols + cols - 1][0],
                           0, vertices[i * cols + cols - 1][2]])

    for i in range(1, rows):
        base_faces.append((cols * i + cols - 1, len(vertices) +
                           (i - 1) + rows, cols * (i - 1) + cols - 1))
        base_faces.append((len(vertices) + i + rows,
                           len(vertices) + (i - 1) + rows, cols * i + cols - 1))

    for i in range(cols):
        base_verts.append([vertices[i][0], 0, vertices[i][2]])

    for i in range(1, cols):
        base_faces.append((i, len(vertices) + (i - 1) + rows + rows, i - 1))
        base_faces.append((len(vertices) + i + rows + rows,
                           len(vertices) + (i - 1) + rows + rows, i))

    for i in range(cols):
        base_verts.append([vertices[(rows - 1) * cols + i][0],
                           0, vertices[(rows - 1) * cols + i][2]])

    for i in range(1, cols):
        base_faces.append(((rows - 1) * cols + i - 1, len(vertices) +
                           (i - 1) + rows + rows + cols, (rows - 1) * cols + i))
        base_faces.append(((rows - 1) * cols + i, len(vertices) + (i - 1) +
                           rows + rows + cols, len(vertices) + i + rows + rows + cols))

    bottom_start = len(base_verts) + len(vertices)

    for i in range(rows * cols):
        base_verts.append([vertices[i][0], 0, vertices[i][2]])

    def generator():
        for i in range(1, rows):
            for j in range(1, cols):
                ul = (i - 1) * cols + j - 1 + bottom_start
                ur = (i - 1) * cols + j + bottom_start
                ll = i * cols + j - 1 + bottom_start
                lr = i * cols + j + bottom_start
                yield (ur, ll, ul)
                yield (lr, ll, ur)
    base_faces.extend(list(generator()))

    vertices = np.concatenate((vertices, np.array(base_verts)), axis=0)
    faces = faces + base_faces

    return vertices, faces
