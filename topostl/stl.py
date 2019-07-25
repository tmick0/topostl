import struct

def write_stl(vertices, triangles, fh):
    fh.write(b'\0' * 80)
    fh.write(struct.pack('<I', len(triangles)))
    for a, b, c in triangles:
        fh.write(struct.pack('<fff', 0, 0, 0))
        fh.write(struct.pack('<fff', *vertices[a]))
        fh.write(struct.pack('<fff', *vertices[b]))
        fh.write(struct.pack('<fff', *vertices[c]))
        fh.write(struct.pack('<H', 0))
