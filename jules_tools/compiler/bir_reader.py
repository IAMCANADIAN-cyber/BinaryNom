import struct
import zlib

class BirReader:
    def __init__(self, f):
        self.f = f
        self.sections = {}

        magic = f.read(4)
        if magic != b'CDIR':
            raise ValueError("Not a BIR file")

        major, minor = struct.unpack('<BB', f.read(2))
        if major != 1 or minor != 0:
            raise ValueError(f"Unsupported BIR version: {major}.{minor}")

        section_count = struct.unpack('<H', f.read(2))[0]

        for _ in range(section_count):
            section_type, flags, _, length, offset = struct.unpack('<BBHQl', f.read(16))
            self.sections[section_type] = {
                'flags': flags,
                'length': length,
                'offset': offset
            }

    def read_section(self, section_type):
        if section_type not in self.sections:
            return None

        section = self.sections[section_type]
        self.f.seek(section['offset'])
        data = self.f.read(section['length'])

        if section['flags'] & 1: # compressed
            data = zlib.decompress(data)

        return data
