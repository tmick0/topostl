from .srtm import srtm3_load, srtm_get_nominal_coords, srtm_resolve_coords
from math import floor
import numpy as np
import itertools
import os

# TODO: remove assumptions about 3 arcsecond resolution


class loader (object):

    def __init__(self, source_dir):
        self._source_dir = source_dir

    def generate(self, north, south, west, east):

        # first, patch together the set of 1 degree rasters which the bounding box spans
        blocks = []
        for lat in np.arange(north, south, -1):
            row = []
            for lon in np.arange(west, east, 1):
                nlat, nlon, data = srtm3_load(os.path.join(
                    self._source_dir, srtm_resolve_coords(lat, lon)))
                row.append(data[1:, :-1])
            blocks.append(row)
        patch = np.block(blocks)

        # now, crop out the region we actually want
        r0 = 1200 - int((north - floor(north)) * 1200)
        c0 = int((west - floor(west)) * 1200)
        rows = int((north - south) * 3600 // 3 + 1)
        cols = int((east - west) * 3600 // 3 + 1)
        res = patch[r0:r0+rows, c0:c0+cols]
        return res
