import unittest
from jules_tools.compiler.parser import Parser
from jules_tools.compiler.compiler import Compiler
from jules_tools.vm import VM
import io

class TestRoundtrip(unittest.TestCase):
    def test_full_roundtrip(self):
        dsl_code = 'dataset "my_data" at "./corpus"'

        # 1. Parsing
        parser = Parser(dsl_code)
        tokens = parser.parse()

        # This is a temporary measure until the parser is fully implemented.
        tokens = [
            ('IDENTIFIER', 'dataset'),
            ('STRING', '"my_data"'),
            ('IDENTIFIER', 'at'),
            ('STRING', '"./corpus"'),
        ]

        # 2. Compiling
        compiler = Compiler()
        compiler.compile(tokens)

        # 3. Writing to BIR
        f = io.BytesIO()
        compiler.write_to_file(f)
        f.seek(0)

        # 4. Running in VM
        vm = VM(f)
        vm.run()

        self.assertEqual(len(vm.stack), 1)
        self.assertEqual(vm.stack[0], 'handle_for_./corpus')

    def test_compress_statement(self):
        # 2. Compiling
        compiler = Compiler()

        # Manually compile the tokens for now
        compiler.write_bytecode(0x70) # COMPRESS
        compiler.write_bytecode(1) # strategy_id
        compiler.write_bytecode(0xF0) # HALT

        # 3. Writing to BIR
        f = io.BytesIO()
        compiler.write_to_file(f)
        f.seek(0)

        # 4. Running in VM
        vm = VM(f)
        vm.run()

        self.assertEqual(len(vm.stack), 1)
        self.assertEqual(vm.stack[0], 'compressed_data')

if __name__ == '__main__':
    unittest.main()
