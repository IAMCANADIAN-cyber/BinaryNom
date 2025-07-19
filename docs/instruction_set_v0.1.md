# Instruction Set Specification v0.1

This document specifies the initial version of the "Jules VM" instruction set.

## Binary Encoding

The instruction format is as follows:

| Field         | Bits     | Purpose                            |
| ------------- | -------- | ---------------------------------- |
| Opcode        | 8        | Instruction identity               |
| Mode Flags    | 8        | Modifiers (modality, level)        |
| Operand Count | 4        | Small count (0–15)                 |
| Reserved      | 4        | Future                             |
| Operands      | variable | LE encoded ints/floats/string refs |

- **Opcode**: A single byte identifying the instruction.
- **Mode Flags**: Used for instruction modifiers. For v0.1, this is mostly unused and should be set to `0x00`.
- **Operand Count**: The number of operands that follow the instruction header.
- **Reserved**: Must be zero.
- **Operands**: The arguments to the instruction. Operands are variable-length and are encoded using a simple scheme:
    - **Integers**: Encoded as little-endian 32-bit signed integers.
    - **Floats**: Encoded as IEEE 754 single-precision 32-bit floating-point numbers.
    - **String References**: Encoded as a 32-bit unsigned integer index into the constant pool.

## Constant Pool

The constant pool is a separate section in the BIR container. It stores all constant values, such as strings and large numeric values, that are referenced by instructions. This reduces code size and improves cache performance.

## Instruction Set

| Opcode | Mnemonic         | Operands                | Description                                                                                             |
|--------|------------------|-------------------------|---------------------------------------------------------------------------------------------------------|
| 0x00   | `NOP`            |                         | No operation. Used for alignment and patching.                                                          |
| 0x01   | `LOAD_DATASET`   | `cid` (str ref)         | Loads a dataset from the given path (referenced by its index in the constant pool). Pushes handle to stack. |
| 0x05   | `SET_FILTER`     | `mask` (int)            | Sets the ingest filter bitmask for the current dataset.                                                 |
| 0x12   | `OCR_CONF`       | `thr` (float)           | Sets the OCR confidence threshold.                                                                      |
| 0x30   | `EMBED_BATCH`    | `size` (int)            | Sets the batch size for the embedding process.                                                          |
| 0x41   | `CLUSTER`        | `algo_id` (int), `k` (int) | Performs clustering on the embedded data. `algo_id` refers to a predefined algorithm.                 |
| 0x55   | `SUMMARIZE`      | `scope_id` (int), `model_id` (str ref), `temp` (float) | Runs a language model to summarize the data. This will make a call to LM Studio. |
| 0x70   | `COMPRESS`       | `strategy_id` (int)     | Applies a compression strategy to the current data.                                                     |
| 0x90   | `BUILD_CAPSULE`  | `token_budget` (int)    | Assembles the final output capsule with a target token budget.                                          |
| 0xA0   | `WRITE_OUTPUT`   | `file_ref` (str ref)    | Writes the output of the pipeline to a file.                                                            |
| 0xF0   | `HALT`           |                         | Stops the execution of the program.                                                                     |
