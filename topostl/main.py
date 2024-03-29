import argparse
from .loader import loader
from .mesh import create_mesh
from .stl import write_stl
from .normalize import rotate, center, scale, fill


def main():
    parser = argparse.ArgumentParser(
        description="A utility for generating printable meshes of terrain")

    parser.add_argument('-d', '--data', required=True,
                        help="Source elevation model directory")
    parser.add_argument('-n', '--north', type=float,
                        required=True, help="Northern latitude of bounding box")
    parser.add_argument('-s', '--south', type=float,
                        required=True, help="Southern latitude of bounding box")
    parser.add_argument('-w', '--west', type=float, required=True,
                        help="Western longitude of bounding box")
    parser.add_argument('-e', '--east', type=float, required=True,
                        help="Eastern longitude of bounding box")
    parser.add_argument('-f', '--scale', type=float,
                        default=0.00001, help="Scale factor")
    parser.add_argument('-b', '--base', type=float,
                        default=5.0, help="Base thickness (mm)")
    parser.add_argument('-o', '--output', required=True,
                        help="Output STL filename")
    parser.add_argument('-a', '--exaggerate', type=float,
                        default=1.0, help="Scaling factor for elevations")

    args = parser.parse_args()

    l = loader(args.data)
    alts = l.generate(args.north, args.south, args.west, args.east)
    alts *= args.exaggerate
    rows, cols = alts.shape

    vertices, triangles = create_mesh(
        args.north, args.south, args.west, args.east, alts)

    vertices = rotate(args.north, args.south, args.west, args.east, vertices)
    vertices = center(vertices)
    vertices = scale(vertices, args.scale)
    vertices, triangles = fill(vertices, triangles, rows, cols, args.base)

    with open(args.output, 'wb') as fh:
        write_stl(vertices, triangles, fh)
