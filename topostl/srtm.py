import numpy as np
import re
from math import floor

_SRTM_FILENAME_REGEX = re.compile("(?:.*/)?([NS])(\d{2})([EW])(\d{3}).hgt")


def srtm_parse_filename(filename):
    m = _SRTM_FILENAME_REGEX.match(filename)
    if m is None:
        raise ValueError("Could not parse SRTM filename: {}".format(filename))
    s = int(m.group(2)) * (-1 if m.group(1) == 'S' else 1)
    w = int(m.group(4)) * (-1 if m.group(3) == 'W' else 1)
    return s, w


def srtm_get_nominal_coords(lat, lon):
    lat = floor(lat)
    lon = floor(lon)
    return lat, lon


def srtm_resolve_coords(lat, lon):
    lat, lon = srtm_get_nominal_coords(lat, lon)
    ns = 'N' if lat >= 0. else 'S'
    ew = 'E' if lon >= 0. else 'W'
    return "{:s}{:d}{:s}{:d}.hgt".format(ns, abs(lat), ew, abs(lon))


def srtm3_load(filename):
    nlat, nlon = srtm_parse_filename(filename)
    alts = np.fromfile(
        filename, dtype='>i2', count=1201 * 1201).reshape((1201, 1201))
    return nlat, nlon, alts
