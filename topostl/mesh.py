import pyproj
import numpy as np
from .coords import ECEF, LLA


def generate_triangles(rows, cols):
    def generator():
        for i in range(1, rows):
            for j in range(1, cols):
                ul = (i - 1) * cols + j - 1
                ur = (i - 1) * cols + j
                ll = i * cols + j - 1
                lr = i * cols + j
                yield (ul, ll, ur)
                yield (ur, ll, lr)
    return list(generator())


def create_mesh(north, south, west, east, raster):
    rows, cols = raster.shape
    lats = np.linspace(north, south, rows, False)
    lons = np.linspace(west, east, cols, False)

    longrid, latgrid = np.meshgrid(lons, lats)

    x, y, z = pyproj.transform(
        LLA, ECEF, longrid, latgrid, raster, radians=False)

    vertices = np.column_stack((x.flatten(), y.flatten(), z.flatten()))
    triangles = generate_triangles(rows, cols)

    return vertices, triangles
