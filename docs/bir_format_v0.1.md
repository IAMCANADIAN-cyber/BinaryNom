# Binary Intermediate Representation (BIR) Format v0.1

This document specifies the v0.1 of the Binary Intermediate Representation (BIR) format.

## Container Layout

```
Offset  Size  Description
0x00    4     Magic 'CDIR'
0x04    1     Major version
0x05    1     Minor version
0x06    2     Section count (N)
0x08    ...   Section headers (N * 16B):
               type(1B) | flags(1B) | reserved(2B) |
               length(8B) | offset(4B)
[Sections...]
[CRC32 overall]
```

- **Magic**: The 4-byte sequence `CDIR` (Context Distiller IR).
- **Version**: Major and minor version of the BIR format.
- **Section Count**: The number of sections in the container.
- **Section Headers**: A table of section headers, each 16 bytes long.
    - **type**: The type of the section (see below).
    - **flags**: Flags for the section (e.g., compression).
    - **reserved**: Reserved for future use.
    - **length**: The length of the section data in bytes.
    - **offset**: The offset of the section data from the beginning of the file.
- **Sections**: The actual data for each section.
- **CRC32**: A CRC32 checksum of the entire file for integrity checking.

## Section Types (1B)

* 0x01 CONSTANT\_POOL
* 0x02 INSTRUCTION\_STREAM
* 0x03 METADATA (schema, symbol table)
* 0x04 PROMPTS (compressed)
* 0x05 HEURISTICS (YAML→binary map)
* 0x06 MODELS (optional quant params)
* 0x07 NATIVE\_PATCH
* 0x08 PROVENANCE
* 0xFF FOOTER / future

## Provenance Section

The provenance section (`PROV`) stores a mapping from output artifacts (like summary bullets) to their origin chunks of data. This is crucial for auditing and debugging. The exact format of the provenance data will be defined later.
