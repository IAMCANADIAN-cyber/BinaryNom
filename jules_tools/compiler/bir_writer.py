import struct
import zlib

class BirWriter:
    def __init__(self):
        self.sections = []

    def add_section(self, section_type, data, compressed=False):
        if compressed:
            data = zlib.compress(data)
            flags = 1
        else:
            flags = 0
        self.sections.append({
            'type': section_type,
            'flags': flags,
            'data': data
        })

    def write(self, f):
        # Magic and version
        f.write(b'CDIR')
        f.write(struct.pack('<BB', 1, 0))
        f.write(struct.pack('<H', len(self.sections)))

        # Section headers (placeholder)
        header_size = 8 + len(self.sections) * 16
        f.write(b'\x00' * (header_size - f.tell()))

        # Section data
        section_offsets = []
        for section in self.sections:
            section_offsets.append(f.tell())
            f.write(section['data'])

        # Go back and write the real section headers
        f.seek(8)
        for i, section in enumerate(self.sections):
            f.write(struct.pack('<B', section['type']))
            f.write(struct.pack('<B', section['flags']))
            f.write(struct.pack('<H', 0)) # reserved
            f.write(struct.pack('<Q', len(section['data'])))
            f.write(struct.pack('<I', section_offsets[i]))

        # CRC32
        f.seek(0)
        crc = zlib.crc32(f.read())
        f.seek(0, 2) # go to end
        f.write(struct.pack('<I', crc))
