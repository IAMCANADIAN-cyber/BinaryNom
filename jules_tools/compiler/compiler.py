import struct
from .bir_writer import BirWriter

class Compiler:
    def __init__(self):
        self.bytecode = bytearray()
        self.constant_pool = []
        self.provenance = {} # a simple dict for now

    def compile(self, tokens):
        # Placeholder for the full compilation logic
        # In a real implementation, this would be a proper recursive descent parser
        # that builds an AST, which is then traversed to generate bytecode.
        # For now, we'll just do a simple linear scan.

        i = 0
        while i < len(tokens):
            kind, value = tokens[i]
            if kind == 'IDENTIFIER' and value == 'dataset':
                self.write_bytecode(0x01) # LOAD_DATASET
                # In a real implementation, we'd handle errors here
                dataset_name = tokens[i+1][1].strip('"')
                dataset_path = tokens[i+3][1].strip('"')
                const_index = self.add_constant(dataset_path)
                self.write_bytecode(const_index)
                self.provenance[len(self.bytecode)] = f"dataset declaration for {dataset_name}"
                i += 4
            else:
                i += 1

        self.write_bytecode(0xF0) # HALT
        return self.bytecode, self.constant_pool, self.provenance

    def add_constant(self, value):
        if value not in self.constant_pool:
            self.constant_pool.append(value)
        return self.constant_pool.index(value)

    def write_bytecode(self, *args):
        for arg in args:
            if isinstance(arg, int):
                self.bytecode.extend(struct.pack('<I', arg))
            else:
                raise TypeError(f"Unsupported bytecode type: {type(arg)}")

    def write_to_file(self, f):
        writer = BirWriter()

        # Constant Pool
        cp_data = bytearray()
        for const in self.constant_pool:
            if isinstance(const, str):
                b = const.encode('utf-8')
                cp_data.extend(struct.pack('<I', len(b)))
                cp_data.extend(b)

        writer.add_section(0x01, cp_data)
        writer.add_section(0x02, self.bytecode)

        # Provenance
        prov_data = bytearray()
        for offset, description in self.provenance.items():
            b = description.encode('utf-8')
            prov_data.extend(struct.pack('<I', offset))
            prov_data.extend(struct.pack('<I', len(b)))
            prov_data.extend(b)
        writer.add_section(0x08, prov_data)

        writer.write(f)
